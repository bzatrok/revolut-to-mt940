from datetime import datetime
from data import Transaction
from constants import *

class Mt940Writer:
    def __init__(self, filename, account_iban, month):
        self.file = open(filename, 'w')
        self.account_iban = account_iban
        self._write_header(month)
        self._written_starting_balance = False
        self._written_ending_balance = False
        self._balance = None
        self._date = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def write_transaction(self, transaction: Transaction):
        if not self._written_starting_balance:
            self._write_starting_balance(transaction.datetime, transaction.before_balance)

        self.file.writelines([
            self._make_61(transaction),
            self._make_86(transaction)
        ])

        self._balance = transaction.after_balance
        self._date = transaction.datetime

    def release(self):
        if not self.file.closed:
            if self._written_starting_balance and not self._written_ending_balance:
                self._write_ending_balance()
            self.file.write('-}')
            self.file.close()

    def _write_header(self, month):
        headers = [
            f"{{1:F01{REVOLUT_BIC}XXX0000000000}}",
            f"{{2:I{TAG_940}{REVOLUT_BIC}XXXN}}",
            "{4:",
            f":{TAG_940}:",
            f":20:{TAG_940}{REVOLUT_NAME}-{month}",
            f":25:{self.account_iban} {CURRENCY}",
            f":28C:{DEFAULT_SEQUENCE_NO}"
        ]
        self.file.write('\n'.join(headers) + '\n')

    def _write_starting_balance(self, date, balance):
        self.file.write(
            f":60F:{self._balance_line(date, balance)}\n"
        )
        self._written_starting_balance = True

    def _write_ending_balance(self):
        self.file.write(
            f":62F:{self._balance_line(self._date, self._balance)}\n"
        )
        self._written_ending_balance = True

    def _make_61(self, transaction: Transaction):
        date = transaction.datetime.strftime('%y%m%d')
        entry_date = transaction.datetime.strftime('%m%d')
        dc_mark = 'D' if transaction.amount < 0 else 'C'
        amount = f"{abs(transaction.amount):.2f}".replace('.', ',')
        
        return f":61:{date}{entry_date}{dc_mark}{amount}{NTRF}NONREF\n"

    def _make_86(self, transaction: Transaction):
        return (f":86:/IBAN/{transaction.iban or ''}"
                f"/NAME/{transaction.name or ''}"
                f"/REMI/{transaction.description or ''}\n")

    def _balance_line(self, date, balance):
        sign = 'D' if balance < 0 else 'C'
        date_str = date.strftime('%y%m%d')
        amount = f"{abs(balance):.2f}".replace('.', ',')
        return f"{sign}{date_str}{CURRENCY}{amount}"