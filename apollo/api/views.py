import secrets

import botocore
import requests
import urllib.parse
import hashlib
import hmac
import sys

from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.utils import timezone
from ipware import get_client_ip

from django.http import HttpResponse, JsonResponse
from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import AllowAny

from apollo.api import helpers
from apollo.api.models import StoreTransaction, StoreCurrency, StoreTransactionStatus, StoreVariables
from apollo.api.serializers import StoreTransactionSerializer, StoreVariablesSerializer

MENTION_RE = '@[a-zA-Z0-9_]*'
SORT_METHODS = ['HOT', 'NEW', 'OLD']


class IPNCallbackView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # ipn_version	1.0
        # ipn_type	Currently: 'simple, 'button', 'cart', 'donation', 'deposit', 'withdrawal', or 'api'
        # ipn_mode	Currently: 'hmac'
        # ipn_id	The unique identifier of this IPN
        # merchant	Your merchant ID
        print('received IPN')

        if 'HMAC' not in request.headers:
            return helpers.bad_request()

        raw_request = request.body.decode('utf8')
        print(raw_request)
        if not raw_request:
            return helpers.bad_request()

        if 'merchant' not in request.data:
            return helpers.bad_request()

        if request.data['merchant'] != settings.COINPAYMENTS_MERCHANT_ID:
            return HttpResponse(content='Merchant not authorized', status=403)

        hmac_signature = hmac.new(settings.COINPAYMENTS_IPN_SECRET.encode('utf8'), raw_request.encode('utf8'),
                                  hashlib.sha512)
        if request.headers['HMAC'] != hmac_signature.hexdigest():
            return HttpResponse(content='HMAC signature mismatch', status=403)

        if request.data['ipn_type'] == 'api':
            transaction = StoreTransaction.objects.filter(id=request.data['txn_id']).first()
            if transaction is None:
                raise Http404()

            previous_status = transaction.tx_status

            if 'received_amount' in request.data:
                transaction.received_amount = float(request.data['received_amount'])

            if 'received_confirms' in request.data:
                transaction.received_confirmations = int(request.data['received_confirms'])

            status = int(request.data['status'])
            if status == -1:
                transaction.tx_status = StoreTransactionStatus.CANCELLED
            elif status == 0:
                transaction.tx_status = StoreTransactionStatus.AWAITING_PAYMENT
            elif status == 1:
                transaction.tx_status = StoreTransactionStatus.AWAITING_CONFIRMATIONS

                if previous_status == StoreTransactionStatus.AWAITING_PAYMENT:
                    transaction.received_at = timezone.now()
            elif status >= 100:
                transaction.tx_status = StoreTransactionStatus.PAYMENT_COMPLETE

                print('======================    test    ======================')
                print(transaction.received_confirmations)
                print(transaction.confirmations_needed)
                print(transaction.received_amount)
                print(transaction.crypto_amount)
                print((float(transaction.received_amount) >= float(transaction.crypto_amount)))

                if transaction.received_confirmations >= transaction.confirmations_needed and float(transaction.received_amount) >= float(transaction.crypto_amount):
                    print('creating gift card...')
                    store_credit = round((float(transaction.crypto_amount / transaction.exchange_rate) + sys.float_info.epsilon) * 100) / 100
                    print(store_credit)

                    tebex_response = requests.post('https://plugin.tebex.io/gift-cards', json={
                        'amount': store_credit,
                        'note': 'Crypto Exchange #' + transaction.id
                    }, headers={
                        'X-Tebex-Secret': settings.TEBEX_SERVER_SECRET
                    })

                    if tebex_response.status_code == 200:
                        print('worked')
                        tebex_data = tebex_response.json()
                        transaction.gift_card = tebex_data['data']['code']
                    else:
                        tebex_data = tebex_response.json()
                        print('failed error ' + tebex_data['error_code'] + ' ' + tebex_data['error_message'])

            transaction.last_updated = timezone.now()
            transaction.save()

        return HttpResponse(status=200)


class GetStoreVariablesView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return JsonResponse(dict(StoreVariablesSerializer(StoreVariables.load()).data))


class GetExchangeRateView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        if 'currency' not in request.query_params:
            return helpers.bad_request()

        if request.query_params['currency'] not in StoreCurrency:
            return HttpResponse(content='Invalid currency', status=400)

        currency = request.query_params['currency']

        exchange_rate = apps.get_app_config('api').exchange_rates[currency]
        if exchange_rate is None:
            return HttpResponse(content='Server error', status=500)

        return JsonResponse({'rate': exchange_rate})


class CreateTransactionView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        ip_address, is_routable = get_client_ip(request)
        if ip_address is None:
            return HttpResponse(content='Client error', status=400)

        if 'currency' not in request.data:
            return helpers.bad_request()

        if 'amount' not in request.data:
            return helpers.bad_request()

        if 'exchange_rate' not in request.data:
            return helpers.bad_request()

        if 'buyer_email' not in request.data:
            return helpers.bad_request()

        if request.data['currency'] not in StoreCurrency:
            return HttpResponse(content='Invalid currency', status=400)

        try:
            amount = float(request.data['amount'])
        except ValueError:
            return HttpResponse(content='Invalid amount', status=400)

        if amount < 0:
            return HttpResponse(content='Invalid amount', status=400)

        currency = request.data['currency']
        exchange_rate = apps.get_app_config('api').exchange_rates[currency]

        if request.data['exchange_rate'] != exchange_rate:
            return HttpResponse(content='EXCHANGE_RATE_MISMATCH', status=400)

        buyer_email = request.data['buyer_email']
        transaction_id = secrets.token_hex(16)

        modded_currency = currency
        if modded_currency == 'USDT':
            modded_currency = 'USDT.ERC20'

        payload = {
            'key': settings.COINPAYMENTS_PUBLIC_KEY,
            'version': 1,
            'format': 'json',
            'cmd': 'create_transaction',
            'amount': amount,
            'currency1': modded_currency,
            'currency2': modded_currency,
            'buyer_email': buyer_email,
            'item_name': 'Store Credit',
            'item_number': transaction_id,
        }

        payload_bytes = urllib.parse.urlencode(payload).encode('utf8')
        payload_sign = hmac.new(settings.COINPAYMENTS_PRIVATE_KEY.encode('utf8'), payload_bytes,
                                hashlib.sha512).hexdigest()
        payload_headers = {'HMAC': payload_sign}

        api_response = requests.post('https://www.coinpayments.net/api.php', data=payload, headers=payload_headers)
        if api_response.status_code != 200:
            return HttpResponse(content='Server error', status=500)

        api_data = api_response.json()
        if api_data['error'] != 'ok':
            api_error = api_data['error']
            if 'Amount too small' in api_error:
                return HttpResponse(content='Minimum exchange limit! You must send more ' + currency + '!', status=500)

            print('Error creating transaction: ' + api_error)
            return HttpResponse(content='Server error', status=500)

        transaction = StoreTransaction()
        transaction.id = api_data['result']['txn_id']
        transaction.buyer_email = buyer_email
        transaction.currency = currency
        transaction.exchange_rate = exchange_rate
        transaction.crypto_amount = api_data['result']['amount']
        transaction.receiving_address = api_data['result']['address']
        transaction.confirmations_needed = api_data['result']['confirms_needed']

        if 'dest_tag' in api_data['result']:
            transaction.destination_tag = api_data['result']['dest_tag']

        transaction.qr_code_url = api_data['result']['qrcode_url']
        transaction.expires_at = timezone.datetime.fromtimestamp(timezone.now().timestamp() + int(api_data['result']['timeout']))
        transaction.save()

        try:
            html_email = ''
            with open('email_template.txt') as f:
                for line in f.readlines():
                    html_email = html_email + line

            html_email = html_email.replace("{txId}", transaction.id)
            plain_email = 'View your crypto transaction for AkumaMC here: https://crypto.hcrivals.org/transaction/' + transaction.id

            msg = EmailMultiAlternatives(
                subject='AkumaMC - Your Crypto Transaction',
                body=plain_email,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[buyer_email]
            )
            msg.attach_alternative(html_email, "text/html")
            msg.send()
        except Exception as error:
            print('lol email failed')
            print(type(error))

        return JsonResponse(StoreTransactionSerializer(transaction, context={'request': request}).data, safe=False)


class TransactionInfoView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        if 'tx_id' not in request.query_params:
            return helpers.bad_request()

        transaction = StoreTransaction.objects.filter(id=request.query_params['tx_id']).first()
        if transaction is None:
            raise Http404()

        return JsonResponse(StoreTransactionSerializer(transaction).data, safe=False)
