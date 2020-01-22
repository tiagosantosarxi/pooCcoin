import uuid
import json
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


class Wallet:
    """
    Individual user wallet
    Keep track of balance
    Allows a miner to authorize transactions
    """

    def __init__(self):
        self.address = str(uuid.uuid4())
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.balance = STARTING_BALANCE

    def sign(self, data):
        """
        Generate a signature based on the data using the local private key.
        :param data:
        :return: the signed data
        """
        return self.private_key.sign(
            json.dumps(data).encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )

    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify a signature based on the data and the public_key
        :param public_key:
        :param data:
        :param signature:
        :return:
        """
        try:
            public_key.verify(
                signature,
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
