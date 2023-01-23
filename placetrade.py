#!/usr/bin/env python
import time
import json
import hmac
import hashlib
import requests
from urllib.parse import urljoin, urlencode
API_KEY = "a926062397ef774c85f7e7367d74a768d32b51aace21e48e610381e2165358e8"
SECRET_KEY = '650fcdb4fde80c36de24021223cfbe3bb90a8fd3c9aa7ee5a060c8270f8b860f'
BASE_URL = "https://testnet.binancefuture.com"
headers = {
    'X-MBX-APIKEY': API_KEY
}

class BinanceException(Exception):
    def __init__(self, status_code, data):
        self.status_code = status_code
        if data:
            self.code = data['code']
            self.msg = data['msg']
        else:
            self.code = None
            self.msg = None
        message = f"{status_code} [{self.code}] {self.msg}"
        # Python 2.x
        # super(BinanceException, self).__init__(message)
        super().__init__(message)

PATH = "/fapi/v1/order"
timestamp = int(time.time() * 1000)
params = {
        "symbol": "ETHUSDT",
        "side": "BUY",
        'timestamp': timestamp,
        "quantity": 0.1,
        "type": "LIMIT",
        "positionSide":'LONG',
        "timeInForce":'GTC',
        "price":1617.99

}
Stoparams = {
        "symbol": "ETHUSDT",
        "side": "SELL",
        'timestamp': timestamp,
        "quantity": 0.1,
        "type": "STOP_MARKET",
        "positionSide":'LONG',
        "stopPrice":1617.59

}

Profitparams = {
        "symbol": "ETHUSDT",
        "side": "SELL",
        'timestamp': timestamp,
        "quantity": 0.1,
        "type": "TAKE_PROFIT_MARKET",
        "positionSide":'LONG',
        "stopPrice":1617.59

}
query_string = urlencode(params)
params['signature'] = hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
url = urljoin(BASE_URL, PATH)
r = requests.post(url, headers=headers, params=params)


if r.status_code == 200:
    # print(json.dumps(r.json(), indent=2))
    data = r.json()
    print(json.dumps(data, indent=2))
    r = requests.post(url, headers=headers, params=Stoparams)

    if r.status_code == 200:
        # print(json.dumps(r.json(), indent=2))
        data = r.json()
        print(json.dumps(data, indent=2))
    else:
        print(r.status_code,r.json())
    r = requests.post(url, headers=headers, params=Profitparams)

    if r.status_code == 200:
        # print(json.dumps(r.json(), indent=2))
        data = r.json()
        print(json.dumps(data, indent=2))
    else:
        print(r.status_code,r.json())
else:
    print(r.status_code,r.json())


# PATH = '/api/v3/ticker/price'
# params = {
#     'symbol': 'BTCUSDT'
# }
# url = urljoin(BASE_URL, PATH)
# r = requests.get(url, headers=headers, params=params)
# if r.status_code == 200:
#     print(json.dumps(r.json(), indent=2))
# else:
#     raise BinanceException(status_code=r.status_code, data=r.json())
# um_futures_client = UMFutures(key=key, secret=secret)

# try:
#     #response = um_futures_client.balance(recvWindow=6000)
#     response = um_futures_client.api_trading_status(recvWindow=6000)
#     logging.info(response)
# except ClientError as error:
#     logging.error(
#         "Found error. status: {}, error code: {}, error message: {}".format(
#             error.status_code, error.error_code, error.error_message
#         )
#     )
