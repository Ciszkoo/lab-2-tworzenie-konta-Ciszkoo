from datetime import date
import re

from app.SMTPConnection import SMTPConnection


def pesel_processing(pesel):
    if len(pesel) == 11:
        return pesel
    return "Niepoprawny PESEL!"


def is_promo_code_wrong(promo_code):
    if promo_code is None or re.fullmatch("^PROM-.{3}$", promo_code) is None:
        return True
    return False


def is_senior(pesel):
    year_suffix = int(pesel[0:2])
    year_prefix = int(pesel[2:4])

    if (
        pesel == "Niepoprawny PESEL!"
        or year_prefix > 80
        or (year_prefix <= 12 and year_suffix < 61)
    ):
        return True
    return False


def initial_balance(pesel, promo_code):
    if is_promo_code_wrong(promo_code) or is_senior(pesel):
        return 0
    return 50


def isLoanAvailable(history, amount):
    if len(history) >= 5 and sum(history[-5:]) > amount:
        return True
    if len(history) >= 3 and len(list(filter(lambda x: x > 0, history[-3:]))) == 3:
        return True
    return False


class Account:
    express_transfer_commission = 1
    history_mail_content = "Twoja historia konta to: "

    def __init__(self, name, surname, pesel, promo_code=None):
        self.name = name
        self.surname = surname
        self.pesel = pesel_processing(pesel)
        self.balance = initial_balance(self.pesel, promo_code)
        self.transfer_history = []

    def incoming_transfer(self, amount):
        self.balance += amount
        self.transfer_history.append(amount)

    def outgoing_transfer(self, amount):
        if self.balance > amount:
            self.balance -= amount
            self.transfer_history.append(-amount)

    def express_transfer(self, amount):
        if amount <= self.balance:
            self.balance = self.balance - amount - self.express_transfer_commission
            self.transfer_history.extend(
                [-amount, -self.express_transfer_commission])

    def take_loan(self, amount):
        if len(self.transfer_history) < 3:
            return False
        if isLoanAvailable(self.transfer_history, amount):
            self.balance += amount
            return True
        return False

    def send_mail_history(self, mail: str, connector: SMTPConnection) -> bool:
        today = date.today()
        title = f"Wyciąg z dnia {today}"
        content = self.history_mail_content + str(self.transfer_history)
        if connector.send_mail(title, content, mail):
            return True
        return False
