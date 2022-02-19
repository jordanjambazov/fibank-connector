from django.db import models


class Account(models.Model):
    iban = models.CharField(max_length=128)
