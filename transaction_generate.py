import random

# List of cities
cities = ["Delhi","Mangalore","Bangalore","Indore","Lucknow","Jabalpur","Mumbai","Chennai","Kolkata"]

# Function to generate transactions
def generate_transaction():
    order_id = random.randint(1,1000) # 
    point1 = random.choice(cities)
    point2 = random.choice([name for name in cities if name != point1])
    # amount = random.randint(10, 50)  # Random amount between $10 and $50
    return f"package of orderId {order_id} is transported from {point1} to {point2}"
    # return f"{sender} sends ${amount} to {receiver}"

num_transactions = 10000
transactions = [generate_transaction() for _ in range(num_transactions)]

# Save transactions to a text file
with open("transactions.txt", "w") as file:
    for transaction in transactions:
        file.write(transaction + "\n")
