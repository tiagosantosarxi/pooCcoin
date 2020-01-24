from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD_INPUT


class Blockchain:
    """

    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        """
        Add Block to the end of the chain
        :param data:
        :return:
        """
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        """

        :return:
        """
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):
        """
        Replace the local chain with the incoming one if the following applies:
            - The incoming chain is longer than the local one.
            - The incoming chain is formatted properly
        """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. The incoming chain must be longer.')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace invalid chain is invalid: {e}')

        self.chain = chain

    def to_json(self):
        """
        Serialize the blockchain into a list of blocks.
        """
        return list(map(lambda x: x.to_json(), self.chain))

    @staticmethod
    def from_json(json_chain):
        """
        Deserialize a blockchain from json input
        :param json_chain: json input
        :return: blockchain instance
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda x: Block.from_json(x), json_chain))
        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain
        Enforce the following rules of the blockchain:
        - The chain must start with the genesis_block
        - Blocks must be formatted correctly
        """
        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            Block.is_valid_block(last_block, block)
        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        Enforce the rules of a chain composed of blocks of transactions.
            - Each transaction must only appear once in the chain
            - There can only be one mining reward per block.
            - Each transaction must be valid.
        :return:
        """
        transaction_ids = set()
        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False
            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction: {transaction.id} is not unique.')
                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception('There can only be one mining reward per block.')
                    has_mining_reward = True
                else:
                    historic_blockchain = Blockchain()

                    historic_blockchain.chain = chain[0:i]

                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input.get('address')
                    )

                    if historic_balance != transaction.input.get('amount'):
                        raise Exception(f'Transaction {transaction.id} has invalid input amount.')

                Transaction.is_valid_transaction(transaction)


def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    blockchain.add_block('three')

    print(blockchain)


if __name__ == '__main__':
    main()
