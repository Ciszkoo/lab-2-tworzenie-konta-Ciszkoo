import unittest
from parameterized import parameterized

from ..Account import Account


class TestTakingLoan(unittest.TestCase):
    name = "Dariusz"
    surname = "Januszewski"
    pesel = "12325678912"

    def setUp(self):
        self.account = Account(self.name, self.surname, self.pesel)

    @parameterized.expand(
        [
            ([-100, 100, 100, 100], 700, True, 700),
            ([-100, 100, -100, 100], 700, False, 0),
            ([100, 100], 700, False, 0),
            ([-100, -100, 400, -100, 100, -100], 199, True, 199),
            ([-100, -100, 400, -100, 100, -100], 200, False, 0),
            ([400, -100, 100, -100], 200, False, 0),
            ([], 200, False, 0),
        ]
    )
    def test_taking_loan(self, history, amount, expected, balance):
        self.account.transfer_history = history
        is_granted = self.account.take_loan(amount)

        self.assertEqual(is_granted, expected)
        self.assertEqual(self.account.balance, balance)
