# Generated by Django 4.0.2 on 2022-02-19 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=128, unique=True)),
                ('account_entry_serial_number', models.BigIntegerField(unique=True)),
                ('account_balance', models.DecimalField(decimal_places=2, max_digits=11)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=11)),
                ('dtkt', models.CharField(max_length=8)),
                ('time', models.DateTimeField()),
                ('value_time', models.DateTimeField()),
                ('partner', models.CharField(max_length=128)),
                ('beneficiary_order_party', models.CharField(max_length=128)),
                ('transaction_name', models.CharField(max_length=128)),
                ('transaction_account', models.CharField(max_length=64)),
                ('transaction_type', models.CharField(max_length=8)),
                ('transaction_code', models.CharField(max_length=8)),
                ('is_ebank_operation', models.BooleanField()),
                ('is_payment', models.BooleanField()),
                ('load_as_new', models.BooleanField()),
                ('remark_1', models.CharField(max_length=128)),
                ('remark_2', models.CharField(max_length=128)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
            ],
        ),
    ]