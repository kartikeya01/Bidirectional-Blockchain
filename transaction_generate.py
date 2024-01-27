import random

# List of names
names = ["Alice", "Bob", "Charlie", "David", "Emily"]

# Function to generate transactions
def generate_transaction():
    sender = random.choice(names)
    receiver = random.choice([name for name in names if name != sender])
    amount = random.randint(10, 50)  # Random amount between $10 and $50
    return f"{sender} sends ${amount} to {receiver}"

# Generate 1,000,000 transactions
num_transactions = 100
transactions = [generate_transaction() for _ in range(num_transactions)]

# Save transactions to a text file
with open("transactions.txt", "w") as file:
    for transaction in transactions:
        file.write(transaction + "\n")
