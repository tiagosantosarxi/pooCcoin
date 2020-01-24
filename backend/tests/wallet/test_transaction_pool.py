from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain


def test_set_transaction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), 'deadly_recipient', 1)
    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map.get(transaction.id) == transaction


def test_clear_blockchain_transactions():
    transaction_pool = TransactionPool()
    transaction1 = Transaction(Wallet(), 'deadly_recipient', 1)
    transaction2 = Transaction(Wallet(), 'deadly_recipient', 2)
    transaction_pool.set_transaction(transaction1)
    transaction_pool.set_transaction(transaction2)
    blockchain = Blockchain()
    blockchain.add_block([transaction1.to_json(), transaction2.to_json()])

    assert transaction1.id in transaction_pool.transaction_map
    assert transaction2.id in transaction_pool.transaction_map

    transaction_pool.clear_blockchain_transactions(blockchain)

    assert not transaction1.id in transaction_pool.transaction_map
    assert not transaction2.id in transaction_pool.transaction_map
