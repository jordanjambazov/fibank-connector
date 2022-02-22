import logging
import datetime

from django.conf import settings

from account.models import Account
from connector.auth import Auth
from connector.client import Client
from transaction.models import Transaction

logger = logging.getLogger(__name__)


class Engine:
    def __init__(self):
        auth = Auth(settings.FIBANK_USERNAME, settings.FIBANK_PASSWORD)
        self._client = Client(auth)

    def reconcile_all(self):
        self.reconcile_accounts()
        self.reconcile_transactions()

    def reconcile_accounts(self):
        accounts = self._client.get_filtered_accounts()
        for account in accounts:
            db_account, created = Account.objects.get_or_create(
                iban=account['ibanAcNo'],
                defaults={
                    'currency': account['ccy'],
                }
            )
            logger.info(
                'Reconciled account [iban=%s, currency=%s, created=%s]',
                db_account.iban, db_account.currency, created
            )

    def reconcile_transactions(self):
        for db_account in Account.objects.all():
            customer_balance = self._client.get_customer_balance(db_account.iban)
            if not customer_balance:
                logger.warning('Failed to retrieve balance, perhaps API returned 500?')
                continue
            if len(customer_balance['acc']) != 1:
                continue
            statement = customer_balance['acc'][0]['stmt']
            for transaction in statement:
                transaction_type = transaction['trnType']
                if transaction_type in {'OP', 'CL'}:
                    continue
                reference = transaction['reference']
                db_transaction, created = Transaction.objects.get_or_create(
                    account_entry_serial_number=transaction['acEntrySrNo'],
                    defaults={
                        'reference': reference,
                        'account': db_account,
                        'account_balance': transaction['acBal'],
                        'amount': transaction['amount'],
                        'dtkt': transaction['dtkt'],
                        'time': datetime.datetime.strptime(transaction['dateTime'], "%Y-%m-%dT%H:%M:%S%z"),
                        'value_time': datetime.datetime.strptime(transaction['valueDt'], "%Y-%m-%dT%H:%M:%S%z"),
                        'partner': transaction.get('contragent', ''),
                        'beneficiary_order_party': transaction.get('benOrderParty', ''),
                        'transaction_name': transaction.get('trname', ''),
                        'transaction_account': transaction['trnAccount'],
                        'transaction_type': transaction['trnType'],
                        'transaction_code': transaction.get('trnCode', ''),
                        'is_ebank_operation': transaction.get('isEbankOper') == 'Y',
                        'is_payment': transaction.get('isPayment') == 'Y',
                        'load_as_new': transaction.get('loadAsNew') == 'Y',
                        'remark_1': transaction.get('remI', ''),
                        'remark_2': transaction.get('remIi', ''),
                        'remark_3': transaction.get('remIii', ''),
                    }
                )
                logger.info('Reconciled transaction [created=%s]', created)
