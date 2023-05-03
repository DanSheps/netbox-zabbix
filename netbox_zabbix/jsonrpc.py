import json
import logging
import requests

logger = logging.getLogger('netbox.plugins.netbox_zabbix')


class JSONRPC:

    url = None
    username = None
    password = None
    token = None
    id = 1

    ssl_verify = False
    ca_file_path = None
    proxies = None

    def __init__(self, url, username, password, ssl_verify=False, ca_file_path=None, proxies=None):
        self.url = url
        self.username = username
        self.password = password
        self.ssl_verify = ssl_verify
        self.ca_file_path = ca_file_path
        self.proxies = proxies

        if not self.logged_in():
            self.login()

    def send_api_request(self, data):
        if not data.get('id', None):
            data['id'] = self.id
        if not data.get('token', None):
            data['auth'] = self.token
        if not data.get('jsonrpc', None):
            data['jsonrpc'] = '2.0'

        headers = {
            'Content-Type': 'application/json',
        }
        body = json.dumps(data, cls=json.JSONEncoder)
        # Prepare the HTTP request
        params = {
            'method': 'POST',
            'url': self.url,
            'headers': headers,
            'data': body.encode('utf8'),
        }

        try:
            prepared_request = requests.Request(**params).prepare()
        except requests.exceptions.RequestException as e:
            logger.error(f"JSONRPC: Error forming HTTP request: {e}")
            raise e

        with requests.Session() as session:
            session.verify = self.ssl_verify
            if self.ca_file_path:
                session.verify = self.ca_file_path

            response = session.send(prepared_request, proxies=self.proxies)
            self.id += 1

        if 200 <= response.status_code <= 299:
            if response.json().get('error', {}).get('message', None):
                message = response.json().get('error', {}).get('message', None)
                error_data = response.json().get('error', {}).get('data', None)
                logger.debug(f'JSONRPC Result Payload: {data}')
                raise requests.exceptions.RequestException(
                    f"Error {message} returned with data '{error_data}'.  Response: {response.json()}"
                )
            else:
                # logger.info(f"Request succeeded; response status {response.status_code}")
                return response
        else:
            logger.warning(f"JSONRPC: Request failed; response status {response.status_code}: {response.content}")
            logger.debug(f'JSONRPC Result Payload: {data}')
            raise requests.exceptions.RequestException(
                f"Status {response.status_code} returned with content '{response.content}'"
            )

    def logged_in(self):
        if not self.token:
            return False
        return True

    def login(self):
        data = {
            'jsonrpc': '2.0',
            'method': 'user.login',
            'params': {
                'user': self.username,
                'password': self.password
            },
            'id': self.id,
            'auth': self.token
        }
        response = self.send_api_request(data)

        result = response.json()
        self.token = result.get('result', None)
        return result.get('result', None)

    def logout(self):

        data = {
            'jsonrpc': '2.0',
            'method': 'user.logout',
            'params': [],
            'id': self.id,
            'auth': self.token
        }
        response = self.send_api_request(data)

        result = response.json()
        self.auth = None
        return result.get('result', None)
