import requests
import datetime
import hashlib
import urllib
import json

__all__ = ['WELCOME_API_URL', 'WelcomePayments']

T_WELCOME_API_URL = 'https://tpayapi.paywelcome.co.kr/'
WELCOME_API_URL = 'https://payapi.paywelcome.co.kr/'

class WelcomePayments(object):
    def __init__(self, mid, sign_key, mode):
        self.mid = mid
        if mode == 'DEV':
            self.wp_url = T_WELCOME_API_URL
        elif mode == 'DEPLOY':
            self.wp_url = WELCOME_API_URL

        self.mkey = hashlib.sha256(sign_key.encode()).hexdigest()

        requests_session = requests.Session()
        requests_adapters = requests.adapters.HTTPAdapter(max_retries=3)
        requests_session.mount('https://', requests_adapters)
        self.requests_session = requests_session

    class ResponseError(Exception):
        def __init__(self, code=None, message=None):
            self.code = code
            self.message = message

    class HttpError(Exception):
        def __init__(self, code=None, reason=None):
            self.code = code
            self.reason = reason

    @staticmethod
    def get_response(response):
        if response.status_code != 200:
            raise WelcomePayments.HttpError(response.status_code, response.reason)
        result = response.json()
        if result['ResultCode'] != 00:
            raise WelcomePayments.ResponseError(result.get('ResultCode'), result.get('ResultMsg'))
        return result.get('response')

    def get_headers(self):
        return {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}

    def _get(self, url, payload=None):
        headers = self.get_headers()
        response = self.requests_session.get(url, headers=headers, params=payload)
        return self.get_response(response)

    def _post(self, url, payload=None):
        headers = self.get_headers()
        response = self.requests_session.post(url, headers=headers, data=json.dumps(payload))
        return self.get_response(response)

    def cancel(self, **kwargs):
        url = '{}cancel/canel'.format(self.wp_url)
        for key in ['payType', 'Tid', 'price', 'currency']:
            if key not in kwargs:
                raise KeyError('필수 파라미터가 없습니다: %s' % key)
        timestamp = int(datetime.datetime.now().timestamp())
        signature = self.create_signature(timestamp)
        kwargs['timestamp'] = timestamp
        kwargs['signature'] = signature
        return self._post(url, kwargs)

    def create_signature(self, timestamp, **kwargs):
        kwargs['mid'] = self.mid
        kwargs['mkey'] = self.mkey
        kwargs = sorted(dict((k.lower(), v) for k,v in kwargs.items()))
        params = urllib.parse.urlencode(kwargs)
        signature = hashlib.sha256(params.encode()).hexdigest()
        return signature

    def get_bill_key(self, **kwargs):
        url = '{}billing/billkey/card'.format(self.wp_url)
        for key in ['buyerName', 'cardNumber', 'cardExpireYY', 'cardExpireMM', 'registNo', 'passwd']:
            if key not in kwargs:
                raise KeyError('필수 파라미터가 없습니다: %s' % key)
        timestamp = int(datetime.datetime.now().timestamp())
        signature = self.create_signature(timestamp, **{'cardNumber':kwargs['cardNumber']})
        kwargs['timestamp'] = timestamp
        kwargs['signature'] = signature
        return self._post(url, kwargs)

    def bill_pay(self, **kwargs):
        url = '{}billing/billkey/card'.format(self.wp_url)
        for key in ['oid', 'price', 'buyerName', 'billkey']:
            if key not in kwargs:
                raise KeyError('필수 파라미터가 없습니다: %s' % key) 
        timestamp = int(datetime.datetime.now().timestamp())
        signature = self.create_signature(timestamp, **{'oid':kwargs['oid'], 'price':kwargs['price']})
        kwargs['timestamp'] = timestamp
        kwargs['signature'] = signature
        return self._post(url, kwargs)

    def serch_card_prefix(self, **kwargs):
        url = '{}/search/card/prefix'.format(self.wp_url)
        for key in ['cardNumber']:
            if key not in kwargs:
                raise KeyError('필수 파라미터가 없습니다: %s' % key)
        timestamp = int(datetime.datetime.now().timestamp())
        signature = self.create_signature(timestamp, **{'cardNumber':kwargs['cardNumber']})
        kwargs['timestamp'] = timestamp
        kwargs['signature'] = signature
        return self._post(url, kwargs)