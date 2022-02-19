from connector.auth import Auth


class Client:
    api_root = 'https://my.fibank.bg/EBank/api/v1/'

    def __init__(self, auth: Auth):
        self._auth = auth
        self._session = auth.session

    def get_filtered_accounts(self):
        response = self._session.get(
            f'{self.api_root}sywspicklist/sywspicklist/getFilteredAccounts', headers=self._headers()
        )
        assert response.status_code == 200
        return response.json()

    def get_account_statement_list(self):
        response = self._session.get(
            f'{self.api_root}sywsquery/sywsquery/getAccStmtList',
            params={
                'AccountNo': 'BG47FINV91501017006644',
                'FromDate': '2022-02-01T00:00:00%2B0200',
                'Iban': 'BG47FINV91501017006644',
                'ToDate': '2022-02-19T00:00:00%2B0200',
            }
        )
        assert response.status_code == 200
        return response.json()

    def _headers(self):
        return {
            'Accept-Language': 'bg',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {self._auth.access_token}',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'EBank-App-Version': '1',
            'EBank-Client-Time': self._auth.iso_time(),
            'EBank-Cust-Id': '5896443',
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
