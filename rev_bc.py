import os
import hashlib
import random
import json

class Block:
    def __init__(self, transactions, previous_hash, random_number):
        self.transactions = transactions
        self.merkle_root = self.compute_merkle_root()
        self.previous_hash = previous_hash
        self.random_number = random_number
        self.forward_hash = self.compute_forward_hash()

    def compute_merkle_root(self):
        if not self.transactions:
            return hashlib.sha256(''.encode()).hexdigest()

        hashed_transactions = [hashlib.sha256(tx.encode()).hexdigest() for tx in self.transactions]

        while len(hashed_transactions) > 1:
            if len(hashed_transactions) % 2 != 0:
                hashed_transactions.append(hashed_transactions[-1])

            paired_transactions = [(hashed_transactions[i], hashed_transactions[i + 1]) for i in range(0, len(hashed_transactions), 2)]
            hashed_transactions = [hashlib.sha256((tx[0] + tx[1]).encode()).hexdigest() for tx in paired_transactions]

        return hashed_transactions[0]

    def compute_forward_hash(self):
        return hashlib.sha256(self.merkle_root.encode()).hexdigest()

    def compute_block_hash(self):
        block_header = {
            'previous_hash': self.previous_hash,
            'merkle_root': self.merkle_root,
            'random_number': self.random_number
        }
        block_data = {
            'transactions': self.transactions,
            'header': block_header,
            'forward_hash': self.forward_hash
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        # Create a folder named "blockchain"
        self.blockchain_folder = "blockchain"
        os.makedirs(self.blockchain_folder, exist_ok=True)

        # Genesis block (initial block)
        genesis_block = Block(transactions=[], previous_hash='0', random_number=0)
        self.chain.append(genesis_block)

        # Save the genesis block data to a file in the blockchain folder
        genesis_block_filename = os.path.join(self.blockchain_folder, "Block_0.txt")
        with open(genesis_block_filename, 'w') as file:
            file.write("Block Hash: " + genesis_block.compute_block_hash() + "\n")
            file.write("Previous Hash: " + genesis_block.previous_hash + "\n")
            file.write("Merkle Root: " + genesis_block.merkle_root + "\n")
            file.write("Random Number: " + str(genesis_block.random_number) + "\n")
            file.write("Forward Hash: " + genesis_block.forward_hash + "\n")
            file.write("Transactions: {}\n")
            file.write("=" * 50)

    def add_block(self, transactions):
        # Get the previous block's hash
        previous_block_hash = self.chain[-1].compute_block_hash()

        # Generate a random number for the new block
        random_number = random.randint(1, 10**9)

        # Create a new block
        new_block = Block(transactions=transactions, previous_hash=previous_block_hash, random_number=random_number)

        # Add the new block to the chain
        self.chain.append(new_block)

        # Save the block data to a file in the blockchain folder
        block_filename = os.path.join(self.blockchain_folder, f"Block_{len(self.chain) - 1}.txt")
        with open(block_filename, 'w') as file:
            file.write("Block Hash: " + new_block.compute_block_hash() + "\n")
            file.write("Previous Hash: " + new_block.previous_hash + "\n")
            file.write("Merkle Root: " + new_block.merkle_root + "\n")
            file.write("Random Number: " + str(new_block.random_number) + "\n")
            file.write("Forward Hash: " + new_block.forward_hash + "\n")
            file.write("Transactions:\n")
            for tx in new_block.transactions:
                file.write("- " + tx + "\n")
            file.write("=" * 50)

        print(f"New Block is mined. Block data saved to {block_filename}")

    def print_chain(self):
        for i, block in enumerate(self.chain):
            print(f"Block {i}:")
            print("Block Hash:", block.compute_block_hash())
            print("Previous Hash:", block.previous_hash)
            print("Merkle Root:", block.merkle_root)
            print("Random Number:", block.random_number)
            print("Forward Hash:", block.forward_hash)
            print("Transactions:", block.transactions)
            print("=" * 50)

    def traverse_forward(self):
        print("Traversing Forward:")
        for i, block in enumerate(self.chain):
            print(f"Block {i}:")
            print("Block Hash:", block.compute_block_hash())
            print("Previous Hash:", block.previous_hash)
            print("Merkle Root:", block.merkle_root)
            print("Random Number:", block.random_number)
            print("Forward Hash:", block.forward_hash)
            print("Transactions:", block.transactions)
            print("=" * 50)

    def traverse_backward(self):
        print("Traversing Backward:")
        for i in range(len(self.chain) - 1, -1, -1):
            block = self.chain[i]
            print("=" * 50)
            print(f"Block {i}:")
            print("Block Hash:", block.compute_block_hash())
            print("Previous Hash:", block.previous_hash)
            print("Merkle Root:", block.merkle_root)
            print("Random Number:", block.random_number)
            print("Forward Hash:", block.forward_hash)
            print("Transactions:", block.transactions)
            print("=" * 50)

# Read transactions from the text file
with open("sample.txt", "r") as file:
    transactions = file.read().splitlines()

# Create a blockchain and add blocks with transactions
blockchain = Blockchain()

# Define the number of transactions per block
transactions_per_block = 10

# Loop through transactions and create blocks
for i in range(0, len(transactions), transactions_per_block):
    block_transactions = transactions[i:i+transactions_per_block]
    blockchain.add_block(block_transactions)

# Traverse and print the blockchain using forward hashing
blockchain.traverse_forward()

# Traverse and print the blockchain in reverse order using backward hashing
blockchain.traverse_backward()
