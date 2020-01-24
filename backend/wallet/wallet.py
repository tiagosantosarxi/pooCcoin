import uuid
import json
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature


class Wallet:
    """
    Individual user wallet
    Keep track of balance
    Allows a miner to authorize transactions
    """

    def __init__(self, blockchain=None):
        self.address = str(uuid.uuid4())
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.serialize_public_key()
        self.blockchain = blockchain

    @property
    def balance(self):
        return Wallet.calculate_balance(self.blockchain, self.address)

    def sign(self, data):
        """
        Generate a signature based on the data using the local private key.
        :param data:
        :return: the signed data
        """
        return decode_dss_signature(self.private_key.sign(
            json.dumps(data).encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        ))

    def serialize_public_key(self):
        """
        Reset the public key to it's serialized version
        :return:
        """

        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    @staticmethod
    def calculate_balance(blockchain, address):
        """
        Calculate the balance of the given address
        scanning the transaction data within the blockchain
        :param blockchain:
        :param address:
        :return:
        """
        balance = STARTING_BALANCE
        if not blockchain:
            return balance
        for block in blockchain.chain:
            for transaction in block.data:
                if transaction.get('input').get('address') == address:
                    # Any time the address conducts a new transaction it resets it's balance
                    balance = transaction.get('output').get(address)
                elif address in transaction.get('output'):
                    balance += transaction.get('output').get(address)
        return balance

    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify a signature based on the data and the public_key
        :param public_key:
        :param data:
        :param signature:
        :return:
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )
        (r, s) = signature
        try:
            deserialized_public_key.verify(
                encode_dss_signature(r, s),
                json.dumps(data).encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False


def main():
    wallet = Wallet()
    print(f'Wallet: {wallet.__dict__}')


if __name__ == '__main__':
    main()
