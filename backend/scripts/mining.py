import requests
import time
from backend.wallet.wallet import Wallet

BASE_URL = 'http://localhost:5000'


def mine_block():
    return requests.get(f'{BASE_URL}/blockchain/mine').json()


def get_wallet_info():
    return requests.get(f'{BASE_URL}/wallet/info').json()


while True:
    mine_block()
    print(get_wallet_info())
