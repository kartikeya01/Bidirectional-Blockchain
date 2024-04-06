import os
import time
import matplotlib.pyplot as plt

def search_order_id_in_files(folder_path, order_id):
    occurrences = []

    file_list = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    # Iterating over files 
    file_list.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    start_time = time.time()
    for filename in file_list:
        file_path = os.path.join(folder_path, filename)
        
        # Opening the file and searching for occurrences
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                if f"orderId {order_id} " in line:
                    occurrences.append({
                        'file': filename,
                        'line_number': line_number,
                        'line': line.strip()
                    })

    return occurrences , start_time


def plot():
    transactions_per_block = [10,50,100]  # Number of transactions per block
    
    time_in_seconds_uni = [0.069570,0.009841,0.007983]
    time_in_seconds_bi = [0.034785,0.005446,0.003992]

    # Creating the bar chart
    barUni = plt.bar(range(len(transactions_per_block)), time_in_seconds_uni, color='skyblue')
    barBi = plt.bar(range(len(transactions_per_block)), time_in_seconds_bi, color='red')

    # Adding time labels on bars
    for i, bar in enumerate(barUni):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{time_in_seconds_uni[i]:.5f}", ha='center', va='bottom')

    for i, bar in enumerate(barBi):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{time_in_seconds_bi[i]:.5f}", ha='center', va='bottom')

    # Adding labels and title
    plt.xlabel('Number of Transactions per Block')
    plt.ylabel('Time in Seconds')
    plt.title('Comparison of Average Time based on Transactions per Block while tracking')

    # Setting x-axis labels
    plt.xticks(range(len(transactions_per_block)), transactions_per_block)

    # Displaying the plot without gaps between bars
    plt.tight_layout()
    plt.show()

#usage
folder_path = 'blockchain3'
order_id_to_search = 55


result ,start_time= search_order_id_in_files(folder_path, order_id_to_search)
t_elapsed = time.time() - start_time

if result:
    print(f"Occurrences of orderId {order_id_to_search} found in the following files:")
    for occurrence in result:
        print(f"{occurrence['file']} - Line {occurrence['line_number']}: {occurrence['line']}")
    print(f"Time taken : {t_elapsed:.6f}")
    # plot()
else:
    print(f"No occurrences found for orderId {order_id_to_search}.")
