import random
from datetime import datetime, timedelta

def generate_transaction(order_id, entry_type, hub_locations, latest_timestamp):
    random_hours = random.randint(1, 48)
    timestamp = latest_timestamp + timedelta(hours=random_hours)
    
    if entry_type == 'order_placed':
        remark = 'Order Successfully placed'
    elif entry_type == 'shipped':
        source_hub = random.choice(hub_locations)
        destination_hub = random.choice(hub_locations)
        remark = f'Item left {source_hub} moving to {destination_hub}'
    elif entry_type == 'out_for_delivery':
        remark = 'Item is out for delivery'
    elif entry_type == 'delivered':
        remark = 'Item delivered successfully'
    else:
        remark = 'Unknown entry type'

    return f'#{order_id} {entry_type} {timestamp.strftime("%m-%d-%Y %H:%M:%S")} {remark}', timestamp

def generate_transactions(num_entries, hub_locations):
    order_id = 1
    transactions = []
    latest_timestamp = datetime.now()

    entry_types = ['order_placed', 'shipped', 'out_for_delivery', 'delivered']

    for _ in range(num_entries):
        entry_type = entry_types[_ % len(entry_types)]  # Cycle through the entry_types list
        transaction, latest_timestamp = generate_transaction(order_id, entry_type, hub_locations, latest_timestamp)
        transactions.append(transaction)
        
        if entry_type == 'delivered':
            order_id += 1

    return transactions

if __name__ == '__main__':
    num_entries = 100000
    hub_locations = ['Hub1', 'Hub2', 'Hub3', 'Hub4', 'Hub5', 'Hub6', 'Hub7', 'Hub8', 'Hub9', 'Hub10']
    transactions = generate_transactions(num_entries, hub_locations)

    with open('supply_chain.txt', 'w') as file:
        for transaction in transactions:
            file.write(f'{transaction}\n')

    print(f'Transactions saved to supply_chain.txt')
