from connector.auth import Auth


class Client:
    api_root = 'https://my.fibank.bg/EBank/api/v1/'

    def __init__(self, auth: Auth):
        self._auth = auth
        self._session = auth.session
        self._customer_id = self._get_customer_id()

    def _get_customer_id(self):
        response = self._session.get(
            f'{self.api_root}sywsquery/sywsquery/getCustQuery',
            headers=self._headers()
        )
        assert response.status_code == 200
        return response.json()['customer'][0]['ibCustomerId']

    def get_filtered_accounts(self):
        response = self._session.get(
            f'{self.api_root}sywspicklist/sywspicklist/getFilteredAccounts',
            headers=self._headers(include_customer_id=True)
        )
        assert response.status_code == 200
        return response.json()

    def get_customer_balance(self, iban: str):
        response = self._session.get(
            f'{self.api_root}sywsquery/sywsquery/GetCustBal',
            params={
                'FromDate': '1993-02-27T00:00:00%2B0200',  # genesis
                'ToDate': self._auth.iso_time(),
                'Iban': iban,
                'StmtType': 'T',
                'isAccountFromPSD2': 'false',
            },
            headers=self._headers(include_customer_id=True)
        )
        if response.status_code == 500:
            return {}
        assert response.status_code == 200
        return response.json()

    def _headers(self, include_customer_id=False):
        return {
            'Accept-Language': 'bg',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {self._auth.access_token}',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'EBank-App-Version': '1',
            'EBank-Client-Time': self._auth.iso_time(),
            'EBank-Cust-Id': f'{self._customer_id}' if include_customer_id else None,
            'EBank-Device-Id': 'AABBCCDDEE',
            'EBank-Referer': '%2Fizvlechenia%2Facc-stmt-offline',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-platform': "Linux",
            'sec-ch-ua-mobile': '?0',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://my.fibank.bg/EBank/izvlechenia/acc-stmt-offline',
        }
