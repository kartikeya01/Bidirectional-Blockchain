import os
import time
import re

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

folder_path = 'blockchain3'
order_id_to_search = 10000

# Unidirectional Search
result_unidirectional, time_unidirectional = search_order_id_in_files(folder_path, order_id_to_search, bidirectional=False)
if result_unidirectional:
    file_path, position, line = result_unidirectional
    print(f"Unidirectional Search - OrderID {order_id_to_search} found in file: {file_path}, at position: {position}")
    print(f"Line content: {line}")
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
