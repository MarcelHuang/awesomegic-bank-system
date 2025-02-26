# AwesomeGIC Bank System

A simple banking system that supports account transactions, interest calculations, and statement generation.

## Overview

The AwesomeGIC Bank System is a command-line application that allows users to:
- Record deposits and withdrawals for various accounts
- Define interest rate rules that change over time
- Calculate daily interest based on balances and applicable rates
- Generate monthly account statements with interest

## Design and Assumptions

### Core Components

1. **Transaction Class**: Represents individual financial operations (deposits, withdrawals, interest)
   - Supports three transaction types: Deposit (D), Withdrawal (W), and Interest (I)
   - Automatically rounds monetary values to 2 decimal places
   - Handles transaction IDs for tracking

2. **InterestRule Class**: Defines interest rate rules effective from specific dates
   - Supports changing interest rates over time
   - Rules are date-based and sorted chronologically

3. **BankAccount Class**: Manages transactions for a specific account
   - Tracks all transactions for an account
   - Calculates balance at any given date
   - Ensures withdrawals cannot exceed available balance

4. **BankSystem Class**: Main system orchestrating all operations
   - Manages multiple accounts and interest rules
   - Handles transaction creation and validation
   - Calculates daily interest based on the applicable rule
   - Generates statements and reports

### Key Assumptions

- Interest is calculated daily and applied at the end of each month
- Interest calculation uses the actual/365 day basis (daily interest = annual rate / 365)
- Interest is calculated on the daily closing balance
- Interest rules are effective from their defined date until superseded by a new rule
- Transactions are processed in the order they are entered, with a unique ID format (YYYYMMDD-NN)
- Account balances cannot go negative (withdrawals are rejected if they would cause negative balance)
- All monetary values are stored with 2 decimal places precision

## Environment Requirements

The application can run on:
- Windows
- Linux
- macOS

### Prerequisites

- Python 3.6 or higher
- No external dependencies required (only standard library modules)

## Running the Application

1. Ensure Python 3 is installed on your system
2. Clone the repository:
   ```bash
   git clone https://github.com/MarcelHuang/awesomegic-bank-system
   ```
3. Open a terminal or command prompt
4. Navigate to the cloned repository directory
5. Run the following command:

```bash
python bank_system.py
```

## Menu Options

The application provides four main options:

- **[T] Input transactions**: Add deposits or withdrawals to accounts
- **[I] Define interest rules**: Set up interest rate rules with effective dates
- **[P] Print statement**: Generate account statements for specific months
- **[Q] Quit**: Exit the application

## Test Coverage

The system includes comprehensive tests written in both unittest and pytest frameworks:

### Transaction Tests
- Verify proper initialization of Transaction objects
- Confirm proper rounding of monetary values
- Test uppercase conversion of transaction types
- Validate transaction ID handling

### InterestRule Tests
- Test initialization and formatting of interest rules
- Validate proper rounding of interest rates

### BankAccount Tests
- Test adding transactions to accounts
- Verify correct balance calculation across various dates
- Test withdrawal validation (preventing negative balances)

### BankSystem Tests
- Test transaction creation with validation
- Validate interest rule management
- Test interest calculation for:
  - Simple interest scenarios
  - Multiple transactions within a month
  - Changing interest rules
  - Multiple months
- Test reporting functions

### Integration Tests
- Full month scenarios with multiple transactions and interest calculation
- Multi-month scenarios to verify compounding interest

### Main Function Test
- Tests CLI interface with mocked inputs and outputs

## Running the Tests

### Using unittest
Save the test file as `bank_system_tests.py` in the same directory as `bank_system.py` and run:

```bash
python -m unittest bank_system_tests.py
```

### Using pytest
Save the test file as `bank_system_pytest.py` in the same directory as `bank_system.py` and run:

```bash
pytest bank_system_pytest.py -v
```

## Sample Test Run

### Input:

```
T
20230505 AC001 D 100
20230601 AC001 D 150
20230626 AC001 W 20
20230626 AC001 W 100
I
20230101 RULE01 1.95
20230520 RULE02 1.90
20230615 RULE03 2.20
P
AC001 202306
Q
```

### Output:

```
> python bank_system.py
Welcome to AwesomeGIC Bank! What would you like to do?
[T] Input transactions
[I] Define interest rules
[P] Print statement
[Q] Quit
> T
Please enter transaction details in <Date> <Account> <Type> <Amount> format
(or enter blank to go back to main menu):
> 20230505 AC001 D 100
Account: AC001
| Date     | Txn Id      | Type | Amount |
| 20230505 | 20230505-01 | D    | 100.00 |
Is there anything else you'd like to do?
Please enter transaction details in <Date> <Account> <Type> <Amount> format
(or enter blank to go back to main menu):
> 20230601 AC001 D 150
Account: AC001
| Date     | Txn Id      | Type | Amount |
| 20230505 | 20230505-01 | D    | 100.00 |
| 20230601 | 20230601-01 | D    | 150.00 |
Is there anything else you'd like to do?
Please enter transaction details in <Date> <Account> <Type> <Amount> format
(or enter blank to go back to main menu):
> 20230626 AC001 W 20
Account: AC001
| Date     | Txn Id      | Type | Amount |
| 20230505 | 20230505-01 | D    | 100.00 |
| 20230601 | 20230601-01 | D    | 150.00 |
| 20230626 | 20230626-01 | W    |  20.00 |
Is there anything else you'd like to do?
Please enter transaction details in <Date> <Account> <Type> <Amount> format
(or enter blank to go back to main menu):
> 20230626 AC001 W 100
Account: AC001
| Date     | Txn Id      | Type | Amount |
| 20230505 | 20230505-01 | D    | 100.00 |
| 20230601 | 20230601-01 | D    | 150.00 |
| 20230626 | 20230626-01 | W    |  20.00 |
| 20230626 | 20230626-02 | W    | 100.00 |
Is there anything else you'd like to do?
Please enter transaction details in <Date> <Account> <Type> <Amount> format
(or enter blank to go back to main menu):
> 
[T] Input transactions
[I] Define interest rules
[P] Print statement
[Q] Quit
> I
Please enter interest rules details in <Date> <RuleId> <Rate in %> format
(or enter blank to go back to main menu):
> 20230101 RULE01 1.95
Interest rules:
| Date     | RuleId | Rate (%) |
| 20230101 | RULE01 |     1.95 |
Is there anything else you'd like to do?
Please enter interest rules details in <Date> <RuleId> <Rate in %> format
(or enter blank to go back to main menu):
> 20230520 RULE02 1.90
Interest rules:
| Date     | RuleId | Rate (%) |
| 20230101 | RULE01 |     1.95 |
| 20230520 | RULE02 |     1.90 |
Is there anything else you'd like to do?
Please enter interest rules details in <Date> <RuleId> <Rate in %> format
(or enter blank to go back to main menu):
> 20230615 RULE03 2.20
Interest rules:
| Date     | RuleId | Rate (%) |
| 20230101 | RULE01 |     1.95 |
| 20230520 | RULE02 |     1.90 |
| 20230615 | RULE03 |     2.20 |
Is there anything else you'd like to do?
Please enter interest rules details in <Date> <RuleId> <Rate in %> format
(or enter blank to go back to main menu):
> 
[T] Input transactions
[I] Define interest rules
[P] Print statement
[Q] Quit
> P
Please enter account and month to generate the statement <Account> <Year><Month>
(or enter blank to go back to main menu):
> AC001 202306
Account: AC001
| Date     | Txn Id      | Type | Amount | Balance |
| 20230601 | 20230601-01 | D    | 150.00 |  250.00 |
| 20230626 | 20230626-01 | W    |  20.00 |  230.00 |
| 20230626 | 20230626-02 | W    | 100.00 |  130.00 |
| 20230630 |             | I    |   0.39 |  130.39 |
Is there anything else you'd like to do?
Please enter account and month to generate the statement <Account> <Year><Month>
(or enter blank to go back to main menu):
> 
[T] Input transactions
[I] Define interest rules
[P] Print statement
[Q] Quit
> Q
Thank you for banking with AwesomeGIC Bank.
Have a nice day!
```

The example shows the system's capabilities in handling multiple transactions, interest rule changes, and correctly calculating interest across different periods.
