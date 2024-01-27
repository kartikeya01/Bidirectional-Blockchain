# import os

# def search_order_id_in_files(folder_path, order_id):
#     last_occurrence = None

#     for filename in os.listdir(folder_path):
#         if filename.endswith(".txt"):
#             file_path = os.path.join(folder_path, filename)

#             with open(file_path, 'r') as file:
#                 lines = file.readlines()

#                 for line_number, line in enumerate(reversed(lines), 1):
#                     if f"orderId {order_id}" in line:
#                         last_occurrence = (file_path, len(lines) - line_number, line.strip())
#                         break

#     return last_occurrence


# folder_path = 'blockchain3' 
# order_id_to_search = 635  

# result = search_order_id_in_files(folder_path, order_id_to_search)

# if result:
#     file_path, position, line = result
#     print(f"Last occurrence of orderId {order_id_to_search} found in file: {file_path}, at position: {position}")
#     print(f"Line content: {line}")
# else:
#     print(f"orderId {order_id_to_search} not found in any files.")


import os
import time

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

    # Iterate over all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            # Read the content of the file
            with open(file_path, 'r') as file:
                lines = file.readlines()

                # Iterate over the lines in reverse order to find the last occurrence
                for line_number, line in enumerate(reversed(lines), 1):
                    if f"orderId {order_id}" in line:
                        last_occurrence = (file_path, len(lines) - line_number, line.strip())
                        break

    return last_occurrence

def search_order_id_from_both_ends(folder_path, order_id):
    first_pointer = None
    last_pointer = None

    file_list = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    total_files = len(file_list)

    # Initialize pointers
    first_file_index = 0
    last_file_index = total_files - 1

    while first_pointer is None or last_pointer is None:
        # Search from the first file
        if first_pointer is None and first_file_index <= last_file_index:
            file_path = os.path.join(folder_path, file_list[first_file_index])

            with open(file_path, 'r') as file:
                lines = file.readlines()

                # Iterate over the lines to find the orderId
                for line_number, line in enumerate(lines, 1):
                    if f"orderId {order_id}" in line:
                        first_pointer = (file_path, line_number, line.strip())
                        break

            first_file_index += 1

        # Search from the last file
        if last_pointer is None and last_file_index >= first_file_index:
            file_path = os.path.join(folder_path, file_list[last_file_index])

            with open(file_path, 'r') as file:
                lines = file.readlines()

                # Iterate over the lines in reverse order to find the orderId
                for line_number, line in enumerate(reversed(lines), 1):
                    if f"orderId {order_id}" in line:
                        last_pointer = (file_path, len(lines) - line_number, line.strip())
                        break

            last_file_index -= 1

        # Check if both pointers have been found or if they have crossed
        if first_pointer is not None and last_pointer is not None:
            return first_pointer if first_pointer[1] <= last_pointer[1] else last_pointer
        elif first_file_index > last_file_index:
            return first_pointer

# Example usage:
folder_path = 'blockchain3' # Replace with the actual path to your folder
order_id_to_search = 635  # Replace with the orderId you want to search

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
