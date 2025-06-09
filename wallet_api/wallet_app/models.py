from django.db import models
from uuid import uuid4

class Wallet(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    balance = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet {self.uuid}"