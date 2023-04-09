import unittest

from ..Account import Account
from ..AccountsRegister import AccountsRegister


class TestAccountsRegister(unittest.TestCase):
    name = "Dariusz"
    surname = "Januszewski"
    pesel = "12325678912"

    @classmethod
    def setUpClass(cls):
        account = Account(cls.name, cls.surname, cls.pesel)
        AccountsRegister.add_account(account)

    @classmethod
    def tearDownClass(cls):
        AccountsRegister.accounts = []

    def test_1_adding_first_account(self):
        account = Account(self.name, self.surname, self.pesel)
        AccountsRegister.add_account(account)
        self.assertEqual(AccountsRegister.number_of_accounts(), 2)

    def test_2_adding_second_account(self):
        account = Account(self.name, self.surname, "12325768912")
        AccountsRegister.add_account(account)
        self.assertEqual(AccountsRegister.number_of_accounts(), 3)

    def test_3_searching_for_existing_account(self):
        account = AccountsRegister.find_account("12325768912")
        self.assertEqual(account.pesel, "12325768912")

    def test_4_searching_for_non_existing_account(self):
        account = AccountsRegister.find_account("02325768910")
        self.assertEqual(account, None)
