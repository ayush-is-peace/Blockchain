import hashlib
import json
from time import time, ctime
from urllib.parse import urlparse


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

        # providing a method for registering nodes
        self.nodes = set()

    def new_block(self, proof, previous_hash=None):
        """
        creates a new block and adds it to the chain
        :param proof: <int> The proof given by the proof of work algorithm
        :param previous_hash: (optional) <str> Hash of previous block
        :return: <dict> new block
        """
        block = {
            "index": len(self.chain) + 1,
            "timestamp-unix": time(),
            "datetime": ctime(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }

        # reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        # adds a new transaction to the list of transactions
        """
        Creates a new transaction to go into the next mined block
        :param sender: <str> address of the sender
        :param recipient: <str> address of the recipient
        :param amount: <int> amount
        :return: <int> The index of block that will hold this transaction
        """
        self.current_transactions.append(
            {
                "sender": sender,
                "recipient": recipient,
                "amount": amount,
            }
        )

        return self.last_block["index"] + 1

    def proof_of_work(self, last_proof):
        """
        Simple proof of work algorithm:
        - Find a number p' such that the hash(pp') contains 4 leading zeros, where p is the previous p'
        - p is the previous proof, and p' is the new proof
         :param last_proof: <int>
         :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    def register_node(self,address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of a node eg http://127.0.0.1:5001/things/morethings
        :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc) # netloc is  127.0.0.1:5001 part of the url above


    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof : Does the hash(last_proof,proof) contain 4 leading zeros?
        To adjust the difficulty of the algorithm we can modify the number of leading zeros
        :param last_proof:<int> previous proof
        :param proof:<int> current proof
        :return: <bool> True if correct , False if not.
        """
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        """
        Creates an SHA-256 hash of a block
        :param block:<dict> block
        :return:<str>
        """
        # We must make sure that the dictionary is ordered , or we'll have inconsistent hashes

        block_string = json.dumps(
            block, sort_keys=True
        ).encode()  # converts our dict to json and encodes it to UTF-8
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # returns the last block in the chain
        return self.chain[-1]
