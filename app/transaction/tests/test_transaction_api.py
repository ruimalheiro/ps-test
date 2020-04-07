import uuid

from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from base.models import Transaction


def create_url():
    return reverse('transaction:create-list')


def delete_url(transaction_id):
    return reverse('transaction:list-detail', args=[transaction_id])


def breakdown_url(account_id):
    return reverse('transaction:breakdown-detail', args=[account_id])


def create_sample_transaction(
    expense_type='invoice',
    amount=1000.00,
    date='2020-01-01',
    account_id=uuid.uuid4()
):
    return Transaction.objects.create(
        expense_type=expense_type,
        amount=amount,
        date=date,
        account_id=account_id
    )


class TransactionApiTests(TestCase):
    def test_create_transaction_successfull(self):
        payload = {
            'expense_type': 'invoice',
            'amount': 30.0,
            'date': '2020-01-01',
            'account_id': uuid.uuid4()
        }
        res = self.client.post(create_url(), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        transaction = Transaction.objects.get(id=res.data['id'])

        for key in payload.keys():
            value = payload[key]
            if key == 'date':
                value = datetime.strptime(payload[key], '%Y-%m-%d').date()
            self.assertEqual(value, getattr(transaction, key))

    def test_create_transaction_invalid_data(self):
        payload = {
            'amount': 30.0,
            'date': '2020-01-01',
            'account_id': uuid.uuid4()
        }
        res = self.client.post(create_url(), payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_transaction_successfull(self):
        payload = {
            'expense_type': 'invoice',
            'amount': 30.0,
            'date': '2020-01-01',
            'account_id': uuid.uuid4()
        }
        res = self.client.post(create_url(), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.delete(delete_url(res.data['id']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        transaction = Transaction.objects.get(id=res.data['id'])

        self.assertTrue(transaction.is_deleted)

    def test_breakdown_no_range(self):
        account_id = uuid.uuid4()
        create_sample_transaction()
        create_sample_transaction()
        create_sample_transaction(account_id=account_id,
                                  expense_type='invoice')
        create_sample_transaction(account_id=account_id,
                                  expense_type='invoice')
        create_sample_transaction(account_id=account_id,
                                  expense_type='service')
        create_sample_transaction(account_id=account_id,
                                  expense_type='service')
        res = self.client.get(breakdown_url(account_id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        invoice = {
            'expense_type': 'invoice',
            'num_transactions': 2,
            'amount_sum': 2000.00,
        }
        service = {
            'expense_type': 'service',
            'num_transactions': 2,
            'amount_sum': 2000.00,
        }
        self.assertEqual(len(res.data), 2)

        for r in res.data:
            if r['expense_type'] == 'invoice':
                self.assertEqual(r, invoice)
            else:
                self.assertEqual(r, service)

    def test_breakdown_start_date(self):
        account_id = uuid.uuid4()
        create_sample_transaction()
        create_sample_transaction()
        create_sample_transaction(account_id=account_id,
                                  expense_type='invoice')
        create_sample_transaction(account_id=account_id,
                                  expense_type='invoice',
                                  date='2020-01-02')
        create_sample_transaction(account_id=account_id,
                                  expense_type='service',
                                  date='2020-01-02')
        create_sample_transaction(account_id=account_id,
                                  expense_type='service',
                                  date='2020-01-03')
        res = self.client.get(
            breakdown_url(account_id),
            {'start_date': '2020-01-02'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        invoice = {
            'expense_type': 'invoice',
            'num_transactions': 1,
            'amount_sum': 1000.00,
        }
        service = {
            'expense_type': 'service',
            'num_transactions': 2,
            'amount_sum': 2000.00,
        }

        self.assertEqual(len(res.data), 2)
        for r in res.data:
            if r['expense_type'] == 'invoice':
                self.assertEqual(r, invoice)
            else:
                self.assertEqual(r, service)

    def test_breakdown_end_date(self):
        account_id = uuid.uuid4()
        create_sample_transaction()
        create_sample_transaction(account_id=account_id,
                                  expense_type='service')
        create_sample_transaction(account_id=account_id,
                                  expense_type='invoice')
        create_sample_transaction(account_id=account_id,
                                  expense_type='invoice',
                                  date='2020-01-02')
        create_sample_transaction(account_id=account_id,
                                  expense_type='service',
                                  date='2020-01-02')
        create_sample_transaction(account_id=account_id,
                                  expense_type='service',
                                  date='2020-01-03')
        res = self.client.get(
            breakdown_url(account_id),
            {'end_date': '2020-01-01'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        invoice = {
            'expense_type': 'invoice',
            'num_transactions': 1,
            'amount_sum': 1000.00,
        }
        service = {
            'expense_type': 'service',
            'num_transactions': 1,
            'amount_sum': 1000.00,
        }
        self.assertEqual(len(res.data), 2)
        for r in res.data:
            if r['expense_type'] == 'invoice':
                self.assertEqual(r, invoice)
            else:
                self.assertEqual(r, service)

    def test_breakdown_full_range(self):
        account_id = uuid.uuid4()
        create_sample_transaction()
        create_sample_transaction(account_id=account_id,
                                  expense_type='service')
        create_sample_transaction(account_id=account_id,
                                  expense_type='invoice')
        create_sample_transaction(account_id=account_id,
                                  expense_type='invoice',
                                  date='2020-01-02')
        create_sample_transaction(account_id=account_id,
                                  expense_type='service',
                                  date='2020-01-02')
        create_sample_transaction(account_id=account_id,
                                  expense_type='service',
                                  date='2020-01-03')
        res = self.client.get(
            breakdown_url(account_id),
            {'start_date': '2020-01-02', 'end_date': '2020-01-02'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        invoice = {
            'expense_type': 'invoice',
            'num_transactions': 1,
            'amount_sum': 1000.00,
        }
        service = {
            'expense_type': 'service',
            'num_transactions': 1,
            'amount_sum': 1000.00,
        }
        self.assertEqual(len(res.data), 2)
        for r in res.data:
            if r['expense_type'] == 'invoice':
                self.assertEqual(r, invoice)
            else:
                self.assertEqual(r, service)
