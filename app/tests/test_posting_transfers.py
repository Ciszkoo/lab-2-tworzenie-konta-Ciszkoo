import unittest
from ..Account import Account
from parameterized import parameterized


class TestPostingTransfers(unittest.TestCase):
    name = "Dariusz"
    surname = "Januszewski"
    pesel = "12325678912"  # 12.2012r.

    def test_incoming_transfer(self):
        account = Account(self.name, self.surname, self.pesel)
        account.balance = 300
        account.incoming_transfer(500)

        self.assertEqual(account.balance, 800, "Srodki nie zostaly dodane!")

    @parameterized.expand([
        (300, 500, 300, "Srodki zostaly odjete mimo braku funduszy na koncie!"),
        (1000, 500, 500, "Srodki nie zostaly wyjete z konta!"),
    ])
    def test_outgoing_transfer_with_not_enough_money(self, balance, amount, expected_balance, message):
        account = Account(self.name, self.surname, self.pesel)
        account.balance = balance
        account.outgoing_transfer(amount)

        self.assertEqual(
            account.balance, expected_balance, message
        )
