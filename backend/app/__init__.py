import os
import random
import requests

from flask import Flask, jsonify, request

from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction_pool import TransactionPool
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
transaction_pool = TransactionPool()
wallet = Wallet(blockchain)
pubsub = PubSub(blockchain, transaction_pool)


@app.route('/')
def route_default():
    return 'Welcome to PussyCoin'


@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.clear_blockchain_transactions(blockchain)

    return jsonify(block.to_json())


@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    transaction_data = request.get_json()
    print(transaction_data)
    transaction = transaction_pool.existing_transaction(wallet.address)
    if transaction:
        transaction.update(
            wallet,
            transaction_data.get('recipient'),
            transaction_data.get('amount')
        )
    else:
        transaction = Transaction(
            wallet,
            transaction_data.get('recipient'),
            transaction_data.get('amount')
        )

    pubsub.broadcast_transaction(transaction)

    return jsonify(transaction.to_json())


@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({
        'address': wallet.address,
        'balance': wallet.balance
    })


ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    # PORT = random.randint(5001, 6000)
    result = requests.get(f'http://46.101.142.221:5000/blockchain')
    result_blockchain = Blockchain.from_json(result.json())
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print(f'Successfully synchronized the blockchain')
    except Exception as ex:
        print(f'Error synchronizing the blockchain: {ex}')

app.run(port=PORT)
