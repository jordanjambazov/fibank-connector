import uuid
from datetime import datetime
from urllib import parse

import requests


class Auth:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._session = requests.Session()
        self._public_token = None
        self._access_token = None
        self._fetch_tokens()

    @property
    def public_token(self):
        return self._public_token

    @property
    def access_token(self):
        return self._access_token

    @property
    def session(self):
        return self._session

    def _fetch_tokens(self):
        authorize_state = str(uuid.uuid1())
        self._session.get('https://my.fibank.bg/oauth2-server/login', params={'client_id': 'E_BANK'})
        csrf = self._extract_csrf(
            self._session.get('https://my.fibank.bg/oauth2-server/oauth/authorize', params={
                'response_type': 'token',
                'client_id': 'E_BANK',
                'redirect_uri': '/EBank/',
                'scope': 'E_BANK',
                'state': authorize_state,

            }).text
        )
        self._session.get('https://my.fibank.bg/oauth2-server/api/v1/sywscertificate/fnGetCertsForLogin', params={
            'client_id': 'E_BANK',
            'userName': self._username,
        })
        response = self._session.post(
            'https://my.fibank.bg/oauth2-server/login',
            data={
                'username': self._username,
                'password': self._password,
                'system': '',
                'client_id': 'E_BANK',
                'lang': 'bg',
                'time': self.iso_time(),
                '_csrf': csrf,
                'sig': '',
            }
        )
        access_token_params = response.history[1].headers['Location'].split('#')[1]
        self._access_token = parse.parse_qs(access_token_params)['access_token'][0]
        self._public_token = self._extract_public_token(response.text)

    @staticmethod
    def _extract_csrf(text):
        for line in text.splitlines():
            if '"_csrf"' in line:
                return line.replace('<meta name="_csrf" content="', '').replace('" />', '').strip()

    @staticmethod
    def _extract_public_token(text):
        for line in text.splitlines():
            if '"EBank_publicToken"' in line:
                return line.replace('<meta name="EBank_publicToken" content="', '').replace('" />', '').strip()

    @staticmethod
    def iso_time():
        return datetime.now().isoformat(timespec='seconds') + '+0200'
