import uuid

from datetime import date
from django.db import models


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateField(default=date.today, db_index=True)
    expense_type = models.CharField(
        max_length=15,
        choices=[
            ('invoice', 'Invoice'),
            ('salary', 'Salary'),
            ('services', 'Services'),
            ('office-supplies', 'Office supplies'),
            ('travel', 'Travel')
        ]
    )
    account_id = models.UUIDField(db_index=True)
    amount = models.DecimalField(max_digits=255, decimal_places=2)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.id
