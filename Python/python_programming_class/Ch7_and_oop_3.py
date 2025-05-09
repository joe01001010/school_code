import random

class BankAccount:
    def __init__ (self):
        self.account_number = random.randint(100000, 999999)
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print("Successful withdrawal")
        else:
            print("Insufficient balance")

    def __str__(self):
        return f"Your account number is {self.account_number} and your balance is ${self.balance}"

def main():
    bankAccount1 = BankAccount()
    bankAccount2 = BankAccount()
    bankAccount1.deposit(100)
    bankAccount2.deposit(200)
    bankAccount1.withdraw(50)
    bankAccount2.withdraw(300)
    print(bankAccount1)
    print(bankAccount2)

if __name__ == "__main__":
    main()