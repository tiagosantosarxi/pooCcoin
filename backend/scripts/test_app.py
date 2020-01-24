import requests
import time
from backend.wallet.wallet import Wallet
BASE_URL = 'http://localhost:5000'


def get_blockchain():
    return requests.get(f'{BASE_URL}/blockchain').json()


def get_blokchain_mine():
    return requests.get(f'{BASE_URL}/blockchain/mine').json()


def post_wallet_transaction(recipient, amount):
    return requests.post(
        f'{BASE_URL}/wallet/transact',
        json={
            'recipient': recipient,
            'amount':    amount
        }
    ).json()


start_blockchain = get_blockchain()
print(f'start_blockchain: {start_blockchain}')
recipient = Wallet().address
pwt1 = post_wallet_transaction(recipient, 99)
print(f'\npwt1: {pwt1}')
pwt2 = post_wallet_transaction(recipient, 99)
print(f'\npwt2: {pwt2}')

time.sleep(1)
mined_block = get_blokchain_mine()
print(f'\n mined_block: {mined_block}')
