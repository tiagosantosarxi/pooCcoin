from abc import ABC
import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction

subscribe_key = 'sub-c-11d99220-37f8-11ea-afe9-722fee0ed680'
publish_key = 'pub-c-924dffeb-a641-4aab-bc36-ddbb59bf86ab'

pnconfig = PNConfiguration()
pnconfig.subscribe_key = subscribe_key
pnconfig.publish_key = publish_key

CHANNELS = {
    'TEST':        'TEST',
    'BLOCK':       'BLOCK',
    'TRANSACTION': 'TRANSACTION'
}


class Listener(SubscribeCallback, ABC):

    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transactions(self.blockchain)
                print(f'\n -- Successfully replaced the local chain')
            except Exception as ex:
                print(f'\n -- Did not replace chain: {ex}')
        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print(f'\n Set the new transaction in the pool')


class PubSub:
    """
    Handles the publish/subscribe layer of the application.
    Provides comunication between two nodes of the blockchain network.
    """

    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """
        Publish the message object to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes.
        :param block:
        :return:
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())

    def broadcast_transaction(self, transaction):
        """
        Broadcast a transaction to all nodes
        :param transaction:
        :return:
        """
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())


# def main():
#     pubsub = PubSub()
#     time.sleep(1)
#     pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})
#
#
# if __name__ == '__main__':
#     main()
