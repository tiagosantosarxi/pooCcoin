from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def test_set_transaction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), 'deadly_recipient', 1)
    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map.get(transaction.id) == transaction
