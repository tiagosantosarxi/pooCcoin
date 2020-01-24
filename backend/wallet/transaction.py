import uuid
import time

from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD, MINING_REWARD_INPUT


class Transaction:
    """
    Record of an exchange in currency between one or more recipients
    """

    def __init__(self, sender_wallet=None, recipient=None, amount=None, id=None, output=None, input=None):
        self.id = id or str(uuid.uuid4())
        self.output = output or self.create_output(
            sender_wallet,
            recipient,
            amount
        )
        self.input = input or self.create_input(sender_wallet, self.output)

    def create_output(self, sender_wallet, recipient, amount):
        """
        Create the output data for the transaction
        :param sender_wallet:
        :param recipient:
        :param amount:
        :return:
        """
        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds balance')
        output = {
            recipient:             amount,
            sender_wallet.address: sender_wallet.balance - amount,

        }
        return output

    def create_input(self, sender_wallet, output):
        """
        Create the input data for the transaction and sign the transaction
        :param sender_wallet:
        :param output:
        :return:
        """
        return {
            'timestamp':  time.time_ns(),
            'amount':     sender_wallet.balance,
            'address':    sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature':  sender_wallet.sign(output)
        }

    def update(self, sender_wallet, recipient, amount):
        """
        Update the transaction with existing or new recipient
        :param sender_wallet:
        :param recipient:
        :param amount:
        :return:
        """
        if amount > self.output.get(sender_wallet.address):
            raise Exception('Amount exceeds balance')
        if recipient in self.output:
            self.output[recipient] = self.output.get(recipient) + amount
        else:
            self.output[recipient] = amount

        self.output[sender_wallet.address] = self.output.get(sender_wallet.address) - amount
        self.input = self.create_input(sender_wallet, self.output)

    def to_json(self):
        """
        Serialize transaction to json
        :return:
        """
        return self.__dict__

    @staticmethod
    def from_json(transaction_json):
        """
        Deserialize a transaction's json back into a transaction instance
        :return:
        """
        return Transaction(**transaction_json)

    @staticmethod
    def is_valid_transaction(transaction):
        """
        Validate a transaction
        :param transaction:
        :return:
        """
        if transaction.input == MINING_REWARD_INPUT:
            if list(transaction.output.values()) != [MINING_REWARD]:
                raise Exception('Invalid mining reward')
            # Mining reward is not signed to we need to return right away
            return
        output_total = sum(transaction.output.values())
        if transaction.input.get('amount') != output_total:
            raise Exception('Invalid Transaction output values')
        if not Wallet.verify(
                transaction.input.get('public_key'),
                transaction.output,
                transaction.input.get('signature')
        ):
            raise Exception('Invalid Signature')

    @staticmethod
    def reward_transaction(miner_wallet):
        """
        Generate a reward transaction to award to the miner
        :param miner_wallet:
        :return:
        """
        output = {
            miner_wallet.address: MINING_REWARD
        }
        return Transaction(input=MINING_REWARD_INPUT, output=output)
