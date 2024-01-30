from datetime import datetime
import os
import time
import re
import matplotlib.pyplot as plt
import numpy as np

def search_order_id_in_files(folder_path, order_id, bidirectional=False):
    start_time = time.time()

    if bidirectional:
        result = search_order_id_from_both_ends(folder_path, order_id)
    else:
        result = search_order_id_unidirectional(folder_path, order_id)

    end_time = time.time()
    elapsed_time = end_time - start_time

    return result, elapsed_time

def search_order_id_unidirectional(folder_path, order_id):
    last_occurrence = None

    # Sorting files in the folder
    file_list = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    # Iterate over files in the order they are stored in the folder
    file_list.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))   
    # Iterating over sorted files
    for filename in file_list:
        file_path = os.path.join(folder_path, filename)

        # Reading the content
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Iterating over the lines in reverse order to find the last occurrence
            for line_number, line in enumerate(reversed(lines), 1):
                if re.search(r'\borderId\s{0}\b'.format(order_id), line):
                    last_occurrence = (file_path, len(lines) - line_number, line.strip())
                    break

    return last_occurrence

def search_order_id_from_both_ends(folder_path, order_id):
    first_pointer = None
    last_pointer = None

    # Sorting files in the folder
    file_list = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    # Iterate over files in the order they are stored in the folder
    file_list.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    total_files = len(file_list)
    
    # Initialize pointers
    first_file_index = 0
    last_file_index = total_files - 1

    while first_file_index <= last_file_index:
        # Search from the first file
        file_path_first = os.path.join(folder_path, file_list[first_file_index])

        with open(file_path_first, 'r') as file:
            lines = file.readlines()

            # Iterate over the lines to find the orderId
            for line_number, line in enumerate(lines, 1):
                if re.search(r'\borderId\s{0}\b'.format(order_id), line):
                    first_pointer = (file_path_first, line_number, line.strip())
                    break

        # Search from the last file
        file_path_last = os.path.join(folder_path, file_list[last_file_index])

        with open(file_path_last, 'r') as file:
            lines = file.readlines()

            # Iterate over the lines in reverse order to find the orderId
            for line_number, line in enumerate(reversed(lines), 1):
                if re.search(r'\borderId\s{0}\b'.format(order_id), line):
                    last_pointer = (file_path_last, len(lines) - line_number, line.strip())
                    break

        # Check if both pointers have been found or if they have crossed
        if last_pointer is not None:
            return last_pointer

        if first_file_index < last_file_index:
            # Move pointers towards each other
            first_file_index += 1
            last_file_index -= 1
        else:
            # Stop if pointers meet
            break
    return first_pointer

def plot():
    transactions_per_block = [10,50,100]  # Number of transactions per block
    
    time_in_seconds_uni = [0.078532,0.017338, 0.022078]
    time_in_seconds_bi = [0.004601,0.001838,0.001420]
    # time_in_seconds_bi = [0.011166,0.002292,0.003809,0.002563,0.003174]
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
    plt.title('Comparison of Average Time based on Transactions per Block')

    # Setting x-axis labels
    plt.xticks(range(len(transactions_per_block)), transactions_per_block)

    # Display the plot without gaps between bars
    plt.tight_layout()
    plt.show()


folder_path = 'blockchain3'
order_id_to_search = 55

# Unidirectional Search
result_unidirectional, time_unidirectional = search_order_id_in_files(folder_path, order_id_to_search, bidirectional=False)
if result_unidirectional:
    file_path, position, line = result_unidirectional
    print(f"Unidirectional Search - OrderID {order_id_to_search} found in file: {file_path}, at position: {position}")
    print(f"Line content: {line}")
    plot()
    
else:
    print(f"Unidirectional Search - OrderID {order_id_to_search} not found in any files.")
print(f"Unidirectional Search Time: {time_unidirectional:.6f} seconds\n")

# Bidirectional Search
result_bidirectional, time_bidirectional = search_order_id_in_files(folder_path, order_id_to_search, bidirectional=True)
if result_bidirectional:
    file_path, position, line = result_bidirectional
    print(f"Bidirectional Search - OrderID {order_id_to_search} found in file: {file_path}, at position: {position}")
    print(f"Line content: {line}")
    

else:
    print(f"Bidirectional Search - OrderID {order_id_to_search} not found in any files.")
print(f"Bidirectional Search Time: {time_bidirectional:.6f} seconds")


