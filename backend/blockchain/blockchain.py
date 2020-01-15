from backend.blockchain.block import Block


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


def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    blockchain.add_block('three')

    print(blockchain)


if __name__ == '__main__':
    main()
