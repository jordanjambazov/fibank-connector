from django.conf import settings
from django.http.response import JsonResponse
from transaction.models import Transaction


def all_transactions(request):
    authorization = request.headers.get('Authorization', '').replace('Bearer', '').strip()
    if not authorization:
        return JsonResponse({
            'error': 'Authorization header not provided'
        }, status=401)
    if authorization != settings.AUTH_SECRET:
        return JsonResponse({
            'error': 'Bad authorization'
        }, status=401)
    transactions = Transaction.objects.all().order_by('time')
    return JsonResponse({
        'result': [{
            'account_entry_serial_number': tx.account_entry_serial_number,
            'reference': tx.reference,
            'account_balance': tx.account_balance,
            'amount': tx.amount,
            'dtkt': tx.dtkt,
            'time': tx.time,
            'value_time': tx.value_time,
            'partner': tx.partner,
            'beneficiary_order_party': tx.beneficiary_order_party,
            'transaction_name': tx.transaction_name,
            'transaction_account': tx.transaction_account,
            'transaction_type': tx.transaction_type,
            'transaction_code': tx.transaction_code,
            'is_ebank_operation': tx.is_ebank_operation,
            'is_payment': tx.is_payment,
            'load_as_new': tx.load_as_new,
            'remark_1': tx.remark_1,
            'remark_2': tx.remark_2,
            'remark_3': tx.remark_3,
        } for tx in transactions]
    })
