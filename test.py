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
        self.forward_hash = '0'

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

    def compute_block_hash(self):
        block_header = {
            'previous_hash': self.previous_hash,
            'merkle_root': self.merkle_root,
            'random_number': self.random_number
        }
        #yaha neeche forward hash bhi le rhe the ab nhi le rhe
        block_data = {
            'transactions': self.transactions,
            'header': block_header
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.blockchain_folder = "blockchain"
        os.makedirs(self.blockchain_folder, exist_ok=True)

        genesis_block = Block(transactions=[], previous_hash='0', random_number=random.randint(1, 10**9))
        self.chain.append(genesis_block)

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
        previous_block_hash = self.chain[-1].compute_block_hash()
        random_number = random.randint(1, 10**9)
        #yaha par change hai random number genesis block ka pehle 0 tha ab ham generate kar rhe hai
        new_block = Block(transactions=transactions, previous_hash=previous_block_hash, random_number=random_number)
        self.chain.append(new_block)

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

        print(f"New Block is mined. Block information  is saved to {block_filename}")
        self.update_forward_hashes()

    def print_chain(self):
        for i, block in enumerate(self.chain):
            print("=" * 50)
            print(f"Block {i}:")
            print("Block Hash:", block.compute_block_hash())
            print("Previous Hash:", block.previous_hash)
            print("Merkle Root:", block.merkle_root)
            print("Random Number:", block.random_number)
            print("Forward Hash:", block.forward_hash)
            print("Transactions:", block.transactions)
            print("=" * 50)

    def traverse_forward(self):
        folder_name = 'blockchain2'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        print("Traversing Forward:")
        for i, block in enumerate(self.chain):
            print("=" * 50)
            print(f"Block {i}:")
            print("Block Hash:", block.compute_block_hash())
            print("Previous Hash:", block.previous_hash)
            print("Merkle Root:", block.merkle_root)
            print("Random Number:", block.random_number)
            print("Forward Hash:", block.forward_hash)
            print("Transactions:", block.transactions)
            print("=" * 50)
            file_name = f"block_{i}.txt"
            file_path = os.path.join(folder_name, file_name)

            with open(file_path, 'w') as file:
                file.write("=" * 50 + '\n')
                file.write(f"Block {i}:\n")
                file.write("Block Hash: " + block.compute_block_hash() + '\n')
                file.write("Previous Hash: " + str(block.previous_hash) + '\n')
                file.write("Merkle Root: " + str(block.merkle_root) + '\n')
                file.write("Random Number: " + str(block.random_number) + '\n')
                file.write("Forward Hash: " + str(block.forward_hash) + '\n')
                file.write("Transactions:\n")
                for tx in block.transactions:
                    file.write("- " + tx + "\n")
                file.write("=" * 50)
                file.write("=" * 50 + '\n')
        

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
    # ye ab naya function hai
    def update_forward_hashes(self):
        for i in range(len(self.chain) - 1):
            self.chain[i].forward_hash = hashlib.sha256(''.join(self.chain[i + 1].transactions).encode()).hexdigest()
        self.chain[-1].forward_hash = 0

with open("sample.txt", "r") as file:
    transactions = file.read().splitlines()

reverse_blockchain = Blockchain()
transactions_per_block = 10
for i in range(0, len(transactions), transactions_per_block):
    block_transactions = transactions[i:i+transactions_per_block]
    reverse_blockchain.add_block(block_transactions)

reverse_blockchain.traverse_forward()
# reverse_blockchain.traverse_backward()


