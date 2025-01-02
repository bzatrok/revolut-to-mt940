import os
import string
import csv
import math
import re
from datetime import datetime, timedelta
from data import Transaction
from constants import *

EXPECT_HEADERS = [
    'Date completed (UTC)',
    'Type',
    'Description',
    'Reference',
    'Amount',
    'Fee',
    'Balance',
    'Beneficiary IBAN',
]

NAME_REMOVE_PREFIXES = [
    'Money added from ',
    'To '
]

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = DATE_FORMAT + TIME_FORMAT

FEE_NAME = REVOLUT_NAME
FEE_IBAN = ''
FEE_DESCRIPTION_FORMAT = 'Bank transaction fee {}'
FEE_DATETIME_DELTA = timedelta(seconds=1)

class RevolutCsvReader:
    def __init__(self, filename):
        if not os.path.isfile(filename):
            raise ValueError('File does not exist: {}'.format(filename))

        self.filename = filename
        self.file = open(self.filename, 'r')
        self.reader = csv.DictReader(self.file)
        self._validate()

    def __del__(self):
        if not self.file.closed:
            self.file.close()

    def _validate(self):
        def _sanitize_header(header):
            header = ''.join([c for c in header
                            if c in string.printable])
            return header.strip()

        headers = [_sanitize_header(h) for h in self.reader.fieldnames]
        if any(header not in headers for header in EXPECT_HEADERS):
            raise ValueError('Headers do not match expected Revolut CSV format.')

    def get_all_transactions(self):
        transactions = []
        for row in self.reader:
            transactions = self._parse_transaction(row) + transactions
        return transactions

    def _parse_transaction(self, row):
        def _sanitize_name(name_):
            for remove_prefix in NAME_REMOVE_PREFIXES:
                if name_.startswith(remove_prefix):
                    name_ = name_[len(remove_prefix):]
            return name_

        completed_date_str, type_str, description, reference, amount_str, fee_str, balance_str, iban = \
            [row[header] for header in EXPECT_HEADERS]

        completed_datetime = datetime.strptime(completed_date_str, DATE_FORMAT)
        amount = float(amount_str)
        fee = float(fee_str)
        balance = float(balance_str)

        transaction_without_fee = Transaction(
            amount=amount,
            name=_sanitize_name(description),
            iban=iban,
            description=self._format_description(type_str, description, reference, iban),
            datetime=completed_datetime,
            before_balance=balance - amount - fee,
            after_balance=balance - fee
        )

        batch = [transaction_without_fee]

        if not math.isclose(fee, 0.00):
            fee_transaction = self._make_fee_transaction(
                completed_datetime,
                balance,
                fee
            )
            batch.append(fee_transaction)

        return batch

    def _format_description(self, type_str, description, reference, iban):
        desc_parts = []
        if type_str:
            desc_parts.append(type_str)
        if description:
            desc_parts.append(description)
        if reference:
            desc_parts.append(f"REF: {reference}")
        if iban:
            desc_parts.append(f"IBAN: {iban}")
        
        return ' '.join(desc_parts)

    def _make_fee_transaction(self, completed_datetime, balance, fee):
        return Transaction(
            amount=fee,
            name=FEE_NAME,
            iban=FEE_IBAN,
            description=FEE_DESCRIPTION_FORMAT.format(
                int(completed_datetime.timestamp())),
            datetime=completed_datetime + FEE_DATETIME_DELTA,
            before_balance=balance - fee,
            after_balance=balance
        )