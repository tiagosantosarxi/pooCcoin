import pytest
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def test_transaction():
    sender_wallet = Wallet()
    recipient = 'deadly_recipient'
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)

    assert transaction.output.get(recipient) == amount
    assert transaction.output.get(sender_wallet.address) == sender_wallet.balance - amount
    assert 'timestamp' in transaction.input
    assert transaction.input.get('amount') == sender_wallet.balance
    assert transaction.input.get('address') == sender_wallet.address
    assert transaction.input.get('public_key') == sender_wallet.public_key
    assert Wallet.verify(
        transaction.input.get('public_key'),
        transaction.output,
        transaction.input.get('signature')
    )


def test_transaction_exceeds_balance():
    with pytest.raises(Exception, match='Amount exceeds balance'):
        Transaction(Wallet(), 'deadly_recipient', 9001)


def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'deadly recipient', 50)
    with pytest.raises(Exception, match='Amount exceeds balance'):
        transaction.update(sender_wallet, 'new recipient', 9001)


def test_transaction_update():
    sender_wallet = Wallet()
    first_recipient = 'first_recipient'
    first_amount = 50
    transaction = Transaction(sender_wallet, first_recipient, first_amount)
    next_recipient = 'next_recipient'
    next_amount = 75
    transaction.update(sender_wallet, next_recipient, next_amount)

    assert transaction.output.get(next_recipient) == next_amount
    assert transaction.output.get(sender_wallet.address) == sender_wallet.balance - first_amount - next_amount
    assert Wallet.verify(
        transaction.input.get('public_key'),
        transaction.output,
        transaction.input.get('signature')
    )

    first_again_amount = 25
    transaction.update(sender_wallet, first_recipient, first_again_amount)
    assert transaction.output.get(first_recipient) == first_amount + first_again_amount
    assert transaction.output.get(
        sender_wallet.address) == sender_wallet.balance - first_amount - next_amount - first_again_amount
    assert Wallet.verify(
        transaction.input.get('public_key'),
        transaction.output,
        transaction.input.get('signature')
    )


def test_valid_transaction():
    Transaction.is_valid_transaction(Transaction(Wallet(), 'deadly_recipient', 50))


def test_valid_transaction_invalid_outputs():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    transaction.output[sender_wallet.address] = 9001

    with pytest.raises(Exception, match='Invalid Transaction output values'):
        Transaction.is_valid_transaction(transaction)


def test_valid_transaction_invalid_signature():
    transaction = Transaction(Wallet(), 'recipient', 50)
    transaction.input['signature'] = Wallet().sign(transaction.output)

    with pytest.raises(Exception, match='Invalid Signature'):
        Transaction.is_valid_transaction(transaction)