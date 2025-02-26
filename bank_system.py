from datetime import datetime, timedelta
import calendar
from decimal import Decimal, ROUND_HALF_UP

class Transaction:
    def __init__(self, date, account, transaction_type, amount, txn_id=None):
        self.date = date
        self.account = account
        self.transaction_type = transaction_type.upper()
        self.amount = Decimal(amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.txn_id = txn_id

class InterestRule:
    def __init__(self, date, rule_id, rate):
        self.date = date
        self.rule_id = rule_id
        self.rate = Decimal(rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

class BankAccount:
    def __init__(self, account_id):
        self.account_id = account_id
        self.transactions = []
        
    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        
    def get_balance_at_date(self, target_date):
        """Calculate balance at the end of the given date"""
        balance = Decimal('0')
        for txn in self.transactions:
            if txn.date <= target_date:
                if txn.transaction_type == 'D':
                    balance += txn.amount
                elif txn.transaction_type == 'W':
                    balance -= txn.amount
                elif txn.transaction_type == 'I':
                    balance += txn.amount
        return balance

    def can_withdraw(self, amount, date):
        """Check if withdrawal is possible (balance won't go negative)"""
        current_balance = self.get_balance_at_date(date)
        return current_balance >= amount

class BankSystem:
    def __init__(self):
        self.accounts = {}
        self.interest_rules = []
        self.transaction_counters = {}  # Format: {date: count}
    
    def create_transaction(self, date_str, account_id, txn_type, amount_str):
        # Validate date format
        try:
            date = datetime.strptime(date_str, "%Y%m%d").date()
        except ValueError:
            return False, "Invalid date format. Please use YYYYMMDD format."
        
        # Validate transaction type
        if txn_type.upper() not in ['D', 'W']:
            return False, "Invalid transaction type. Use D for deposit or W for withdrawal."
        
        # Validate amount
        try:
            amount = Decimal(amount_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            if amount <= 0:
                return False, "Amount must be greater than zero."
        except:
            return False, "Invalid amount format."
        
        # Create or get account
        if account_id not in self.accounts:
            self.accounts[account_id] = BankAccount(account_id)
        
        account = self.accounts[account_id]
        
        # Check if withdrawal is possible
        if txn_type.upper() == 'W' and not account.can_withdraw(amount, date):
            return False, "Insufficient funds for withdrawal."
        
        # Generate transaction ID
        date_key = date_str
        if date_key not in self.transaction_counters:
            self.transaction_counters[date_key] = 0
        self.transaction_counters[date_key] += 1
        txn_id = f"{date_str}-{self.transaction_counters[date_key]:02d}"
        
        # Create and add transaction
        transaction = Transaction(date, account_id, txn_type, amount, txn_id)
        account.add_transaction(transaction)
        
        return True, account_id
    
    def add_interest_rule(self, date_str, rule_id, rate_str):
        # Validate date format
        try:
            date = datetime.strptime(date_str, "%Y%m%d").date()
        except ValueError:
            return False, "Invalid date format. Please use YYYYMMDD format."
        
        # Validate rate
        try:
            rate = Decimal(rate_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            if rate <= 0 or rate >= 100:
                return False, "Interest rate must be greater than 0 and less than 100."
        except:
            return False, "Invalid rate format."
        
        # Remove any existing rule for the same date
        self.interest_rules = [rule for rule in self.interest_rules if rule.date != date]
        
        # Add new rule
        rule = InterestRule(date, rule_id, rate)
        self.interest_rules.append(rule)
        
        # Sort rules by date
        self.interest_rules.sort(key=lambda x: x.date)
        
        return True, None
    
    def calculate_interest(self, account_id, year, month):
        """Calculate interest for the given account and month"""
        if account_id not in self.accounts:
            return None
        
        account = self.accounts[account_id]
        
        # Determine the last day of the month
        _, last_day = calendar.monthrange(year, month)
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, last_day).date()
        
        # Get all relevant transactions for this account up to the end of the month
        account_txns = [t for t in account.transactions if t.date <= end_date]
        if not account_txns:
            return None
        
        # Filter out any existing interest transactions for this month
        interest_txns = [t for t in account_txns 
                        if t.transaction_type == 'I' and 
                        t.date.year == year and 
                        t.date.month == month]
        
        if interest_txns:
            # Interest already calculated for this month
            return None
        
        # Find all balance change dates in the month
        balance_change_dates = set()
        for txn in account_txns:
            if start_date <= txn.date <= end_date:
                balance_change_dates.add(txn.date)
        
        # Add interest rule change dates that fall within the month
        for rule in self.interest_rules:
            if start_date <= rule.date <= end_date:
                balance_change_dates.add(rule.date)
        
        # Add the start of the month and start of any interest rules from previous months
        balance_change_dates.add(start_date)
        
        # Sort the dates
        balance_change_dates = sorted(balance_change_dates)
        
        # Calculate interest for each period
        total_interest = Decimal('0')
        
        for i in range(len(balance_change_dates)):
            current_date = balance_change_dates[i]
            
            # Skip if this is the last date in the month
            if current_date == end_date:
                continue
                
            # Determine the end date for this period
            next_date = balance_change_dates[i+1] if i+1 < len(balance_change_dates) else end_date + timedelta(days=1)
            period_end = next_date - timedelta(days=1)
            
            # Calculate number of days in this period
            num_days = (next_date - current_date).days
            
            # Get the balance at the end of the current date
            balance = account.get_balance_at_date(current_date)
            
            # Find the applicable interest rule
            applicable_rule = None
            for rule in self.interest_rules:
                if rule.date <= current_date:
                    applicable_rule = rule
            
            if applicable_rule:
                # Calculate interest for this period
                daily_interest = (balance * applicable_rule.rate / 100 * num_days) / 365
                total_interest += daily_interest
        
        # Round the total interest to 2 decimal places
        total_interest = total_interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        if total_interest > 0:
            # Create an interest transaction for the last day of the month
            interest_txn = Transaction(end_date, account_id, 'I', total_interest)
            account.add_transaction(interest_txn)
            return total_interest
        
        return Decimal('0')
    
    def print_account_transactions(self, account_id, with_balance=False):
        """Print all transactions for an account"""
        if account_id not in self.accounts:
            return f"Account {account_id} does not exist."
        
        account = self.accounts[account_id]
        
        output = [f"Account: {account_id}"]
        
        if with_balance:
            output.append("| Date     | Txn Id      | Type | Amount | Balance |")
        else:
            output.append("| Date     | Txn Id      | Type | Amount |")
        
        # Sort transactions by date and ID
        sorted_txns = sorted(account.transactions, key=lambda x: (x.date, x.txn_id or ""))
        
        running_balance = Decimal('0')
        
        for txn in sorted_txns:
            date_str = txn.date.strftime("%Y%m%d")
            
            if txn.transaction_type == 'D':
                running_balance += txn.amount
            elif txn.transaction_type == 'W':
                running_balance -= txn.amount
            elif txn.transaction_type == 'I':
                running_balance += txn.amount
            
            if with_balance:
                output.append(f"| {date_str} | {txn.txn_id or '':10} | {txn.transaction_type}    | {txn.amount:>6.2f} | {running_balance:>7.2f} |")
            else:
                output.append(f"| {date_str} | {txn.txn_id or '':10} | {txn.transaction_type}    | {txn.amount:>6.2f} |")
        
        return "\n".join(output)
    
    def print_monthly_statement(self, account_id, year_month):
        """Print monthly statement including interest"""
        if account_id not in self.accounts:
            return f"Account {account_id} does not exist."
        
        try:
            year = int(year_month[:4])
            month = int(year_month[4:])
            
            if month < 1 or month > 12:
                return "Invalid month."
                
        except ValueError:
            return "Invalid year/month format. Please use YYYYMM format."
        
        # Calculate interest for this month if it hasn't been calculated yet
        self.calculate_interest(account_id, year, month)
        
        # Get the start and end dates for the month
        _, last_day = calendar.monthrange(year, month)
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, last_day).date()
        
        account = self.accounts[account_id]
        
        # Filter transactions for this month
        month_txns = [t for t in account.transactions if start_date <= t.date <= end_date]
        
        if not month_txns:
            return f"No transactions found for account {account_id} in {year_month}."
        
        output = [f"Account: {account_id}"]
        output.append("| Date     | Txn Id      | Type | Amount | Balance |")
        
        # Sort transactions by date and ID
        sorted_txns = sorted(month_txns, key=lambda x: (x.date, x.txn_id or ""))
        
        # Calculate the starting balance at the beginning of the month
        starting_balance = account.get_balance_at_date(start_date - timedelta(days=1))
        running_balance = starting_balance
        
        for txn in sorted_txns:
            date_str = txn.date.strftime("%Y%m%d")
            
            if txn.transaction_type == 'D':
                running_balance += txn.amount
            elif txn.transaction_type == 'W':
                running_balance -= txn.amount
            elif txn.transaction_type == 'I':
                running_balance += txn.amount
            
            output.append(f"| {date_str} | {txn.txn_id or '':11} | {txn.transaction_type}    | {txn.amount:>6.2f} | {running_balance:>7.2f} |")
        
        return "\n".join(output)
    
    def print_interest_rules(self):
        """Print all interest rules"""
        if not self.interest_rules:
            return "No interest rules defined."
        
        output = ["Interest rules:"]
        output.append("| Date     | RuleId | Rate (%) |")
        
        for rule in self.interest_rules:
            date_str = rule.date.strftime("%Y%m%d")
            output.append(f"| {date_str} | {rule.rule_id} | {rule.rate:>8.2f} |")
        
        return "\n".join(output)

def main():
    bank_system = BankSystem()
    
    print("Welcome to AwesomeGIC Bank! What would you like to do?")
    
    while True:
        print("[T] Input transactions")
        print("[I] Define interest rules")
        print("[P] Print statement")
        print("[Q] Quit")
        choice = input("> ").strip().upper()
        
        if choice == 'T':
            while True:
                print("Please enter transaction details in <Date> <Account> <Type> <Amount> format")
                print("(or enter blank to go back to main menu):")
                transaction_input = input("> ").strip()
                
                if not transaction_input:
                    break
                
                parts = transaction_input.split()
                if len(parts) != 4:
                    print("Invalid input format. Please try again.")
                    continue
                
                date_str, account_id, txn_type, amount_str = parts
                success, message = bank_system.create_transaction(date_str, account_id, txn_type, amount_str)
                
                if success:
                    print(bank_system.print_account_transactions(message))
                else:
                    print(f"Error: {message}")
                
                print("\nIs there anything else you'd like to do?")
        
        elif choice == 'I':
            while True:
                print("Please enter interest rules details in <Date> <RuleId> <Rate in %> format")
                print("(or enter blank to go back to main menu):")
                rule_input = input("> ").strip()
                
                if not rule_input:
                    break
                
                parts = rule_input.split()
                if len(parts) != 3:
                    print("Invalid input format. Please try again.")
                    continue
                
                date_str, rule_id, rate_str = parts
                success, message = bank_system.add_interest_rule(date_str, rule_id, rate_str)
                
                if success:
                    print(bank_system.print_interest_rules())
                else:
                    print(f"Error: {message}")
                
                print("\nIs there anything else you'd like to do?")
        
        elif choice == 'P':
            while True:
                print("Please enter account and month to generate the statement <Account> <Year><Month>")
                print("(or enter blank to go back to main menu):")
                statement_input = input("> ").strip()
                
                if not statement_input:
                    break
                
                parts = statement_input.split()
                if len(parts) != 2:
                    print("Invalid input format. Please try again.")
                    continue
                
                account_id, year_month = parts
                print(bank_system.print_monthly_statement(account_id, year_month))
                
                print("\nIs there anything else you'd like to do?")
        
        elif choice == 'Q':
            print("Thank you for banking with AwesomeGIC Bank.")
            print("Have a nice day!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()