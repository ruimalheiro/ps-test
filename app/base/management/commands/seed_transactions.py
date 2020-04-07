import csv

from django.core.management.base import BaseCommand
from base.models import Transaction


def get_transaction(row):
    return Transaction(
        id=row['id'],
        date=row['date'],
        expense_type=row['expense_type'],
        amount=row['amount'],
        account_id=row['account_id']
    )


def process_csv_in_chunks(filename, chunk_size):
    with open(filename, "r") as csvfile:
        datareader = csv.DictReader(csvfile)
        next(datareader)
        entries = []
        count = 0
        for row in datareader:
            if len(entries) == chunk_size:
                yield (entries, count)
                entries = []
                count = 0
            else:
                entries.append(get_transaction(row))
                count += 1
        if len(entries) > 0:
            yield (entries, count)
    return


class Command(BaseCommand):
    """Django command to seed data"""

    def handle(self, *args, **options):
        self.stdout.write('deleting existing transactions...')
        Transaction.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('transactions deleted'))

        count = 0
        chunk_size = 100000

        for transactions, size in process_csv_in_chunks(
            'backend-exercise-data.csv',
            chunk_size
        ):
            count += size
            Transaction.objects.bulk_create(transactions)
            self.stdout.write(f'inserted {count} transactions...')

        self.stdout.write(self.style.SUCCESS('transactions seeded'))
