from django.db import models


class Transaction(models.Model):
    reference = models.CharField(max_length=128, unique=True)
    account_entry_serial_number = models.BigIntegerField(unique=True)

    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    account_balance = models.DecimalField(decimal_places=2, max_digits=11)
    amount = models.DecimalField(decimal_places=2, max_digits=11)

    dtkt = models.CharField(max_length=8)  # TODO: consider renaming this field. What does dtkt mean?

    time = models.DateTimeField()
    value_time = models.DateTimeField()

    partner = models.CharField(max_length=128)
    beneficiary_order_party = models.CharField(max_length=128)

    transaction_name = models.CharField(max_length=128)
    transaction_account = models.CharField(max_length=64)
    transaction_type = models.CharField(max_length=8)
    transaction_code = models.CharField(max_length=8)

    is_ebank_operation = models.BooleanField()
    is_payment = models.BooleanField()
    load_as_new = models.BooleanField()

    remark_1 = models.CharField(max_length=128)
    remark_2 = models.CharField(max_length=128)
    remark_3 = models.CharField(max_length=128)
