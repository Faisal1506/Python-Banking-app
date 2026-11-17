import json
import os
from datetime import datetime
import math
import hashlib
import hmac
from getpass import getpass

filename1 = "userInfo.json"
filename2 = "userLog.json"

def load(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = json.load(file)
    else:
        data = {}
    return data

users = load(filename1)
user_log = load(filename2)

def save(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def add_log(username, action, amount, recipient=None):
    if username not in user_log:
        user_log[username] = []
    entry = {
        "action": action,
        "amount": amount,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if recipient:
        entry["recipient"] = recipient
    user_log[username].append(entry)
    save(filename2, user_log)

def hashpassword(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)
    return salt.hex(), hashed.hex()


def check_password(password, salt_hex, hash_hex):
    _, new_hash = hashpassword(password, bytes.fromhex(salt_hex))
    return hmac.compare_digest(new_hash, hash_hex)


def get_amount(prompt):
    try:
        amount = round(float(input(prompt)), 2)
    except ValueError:
        print("Enter a Valid Amount")
        return None
    if not math.isfinite(amount) or amount <=0:
        print("Enter a Valid Amount")
        return None
    return amount

def deposit():
    global username
    balance = users[username]["balance"]
    amount = get_amount("How much would you like to deposit: £")
    if amount is None:
        return
    balance += amount
    users[username]["balance"] = balance
    save(filename1, users)
    add_log(username, "deposit", amount)
    print(f"£{amount} has been deposited")
    print(f"New balance: £{balance:.2f}")

def withdraw():
    global username
    balance = users[username]["balance"]
    amount = get_amount("How much would you like to withdraw: £")
    if amount is None:
        return
    if amount > balance:
        print("Balance too low")
        return
    balance -= amount
    users[username]["balance"] = balance
    save(filename1, users)
    add_log(username, "withdraw", amount)
    print(f"£{amount} has been withdrawn")
    print(f"New balance: £{balance:.2f}")

def send_money():
    global username
    balance = users[username]["balance"]
    user_send = input("Enter Username: ")
    if user_send not in users:
        print("User doesn't exist")
        return
    if user_send == username:
        print("Can't send money to Yourself")
        return
    amount = get_amount("How much would you like to send: £")
    if amount is None:
        return
    if amount > balance:
        print("Balance too low")
        return
    while True:
        press = input(f"You're sending £{amount:.2f} to {user_send}. Press N to go back or Y to confirm: ").lower()
        if press == "y":
            balance -= amount
            users[username]["balance"] = balance
            users[user_send]["balance"] += amount
            save(filename1, users)
            add_log(username, "send", amount, recipient=user_send)
            add_log(user_send, "receive", amount, recipient=username)
            print(f"Successfully sent £{amount:.2f} to {user_send}")
            break
        elif press == "n":
            print("Transaction Failed")
            break
        else:
            print("Invalid Option")

while True:
    print("1. Login")
    print("2. Register")
    print("3. EXIT")
    pick = input("Enter 1, 2 Or 3: ")

    if pick == "1":
        username = input("Enter Username: ")
        password = getpass("Enter Password: ")
        if username in users and check_password(password, users[username]["salt"], users[username]["password_hash"]):
            print(f"Welcome {username}")
            while True:
                balance = users[username]["balance"]
                print(f"Balance: £{balance:.2f}")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Send Money")
                print("4. Logout")
                print("5. View Transaction History")
                atm_choice = input("Your choice: ")
                if atm_choice == "1":
                    deposit()
                elif atm_choice == "2":
                    withdraw()
                elif atm_choice == "3":
                    send_money()
                elif atm_choice == "4":
                    print("Logging out...")
                    break
                elif atm_choice == "5":
                    if username in user_log and user_log[username]:
                        for entry in user_log[username]:
                            action = entry["action"]
                            amount = entry["amount"]
                            timestamp = entry["timestamp"]
                            recipient = entry.get("recipient", "")
                            if recipient:
                                print(f"{timestamp}: {action} £{amount:.2f} -> {recipient}")
                            else:
                                print(f"{timestamp}: {action} £{amount:.2f}")
                    else:
                        print("No transactions yet.")
                else:
                    print("Invalid option")
            else:
                print("Username or Password invalid")

    elif pick == "2":
        while True:
            username = input("Enter Username: ")
            if username in users:
                print("Username Taken")
            else:
                while True:
                    password = input("Enter password: ")
                    if len(password) < 6:
                        print("Password must be at least 6 characters")
                    else:
                        salt, password_hash = hashpassword(password)
                        users[username] = {
                            "salt": salt,
                            "password_hash": password_hash,
                            "balance": 0.0
                            }
                        print(f"{username} Created Successfully")
                        save(filename1, users)
                        break
                break

    elif pick == "3":
        print("Closing...")
        exit()

    else:
        print("Invalid option")