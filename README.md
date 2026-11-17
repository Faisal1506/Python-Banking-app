# Python-Banking-app
# Python Banking App

A multi-user command-line banking application written in Python. Users can register, log in, deposit, withdraw, send money to each other and view their transaction history.

## Features

- **Accounts:** register and log in with a unique username and password
- **Transactions:** deposit, withdraw and transfer money between users, with a confirmation step before sending
- **Transaction history:** every transaction is saved with a timestamp and can be viewed per account
- **Input validation:** one shared helper rejects negative, zero, non-numeric and non-finite (`inf`/`nan`) amounts
- **Persistent storage:** accounts and transaction logs are saved to JSON files between sessions

## Security

- Passwords are never stored in plain text. Each password is hashed with **PBKDF2-HMAC-SHA256** (600,000 iterations) and a unique random salt per user.
- Logins are checked with `hmac.compare_digest` to avoid timing attacks.
- Password input at login is hidden with `getpass`.

## Getting started

Requires **Python 3.6+**. No external packages are needed.

```bash
git clone https://github.com/Faisal1506/Python-Banking-App.git
cd Python-Banking-App
python banking.py
```

`userInfo.json` and `userLog.json` are created automatically on first run. They're excluded from Git so that no account data is ever committed.

## Example

```
1. Login
2. Register
3. EXIT
Enter 1, 2 Or 3: 1
Enter Username: alice
Enter Password:
Welcome alice
Balance: £52.00
...
Your choice: 5
2026-11-17 09:38:08: deposit £50.00
2026-11-17 09:38:08: deposit £5.00
2026-11-17 09:38:08: withdraw £3.00
2026-11-17 09:38:08: send £10.00 -> bob
```

## Planned improvements

- Replace JSON storage with an **SQLite** database
- Store money as integer pence (or `Decimal`) to avoid floating-point rounding
- Add unit tests with **pytest**
