from datetime import date
import requests
import os

from .Account import Account


def nip_processing(nip: str) -> str:
    if len(nip) == 10:
        if BusinessAccount.is_nip_valid(nip):
            return nip
        return "Pranie!"
    return "Niepoprawny NIP!"


class BusinessAccount(Account):
    express_transfer_commission = 5
    history_mail_content = "Historia konta Twojej firmy to: "

    def __init__(self, company_name: str, nip: str):
        self.company_name = company_name
        self.nip = nip_processing(nip)
        self.balance = 0
        self.transfer_history = []

    def take_loan(self, amount: int) -> bool:
        if (
            self.balance >= amount * 2
            and len(list(filter(lambda x: x == -1775, self.transfer_history))) > 0
        ):
            self.balance += amount
            return True
        return False

    @staticmethod
    def is_nip_valid(nip: str) -> bool:
        today = date.today()
        url = os.environ.get('BANK_APP_MF_URL')
        req = requests.get(
            f'{url}{nip}?date={today}')
        if req.status_code == 200:
            return True
        return False
