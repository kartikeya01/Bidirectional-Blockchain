import os
import re
import time

def search_with_two_pointers(folder_path, order_id):
    forward_result = ""
    backward_result = ""
    
    # Get the list of files in the specified folder
    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    # Iterate over files in the order they are stored in the folder
    files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    
    print(files)
    print("\n")
    start_time = time.time()
    # Use two pointers to traverse the list of files
    forward_pointer = 0
    backward_pointer = len(files) - 1

    while forward_pointer <= backward_pointer:
        forward_file = files[forward_pointer]
        backward_file = files[backward_pointer]

        # Search for occurrences in the forward file
        forward_file_path = os.path.join(folder_path, forward_file)
        with open(forward_file_path, 'r') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                if re.search(r'\borderId\s{0}\b'.format(order_id), line):
                    forward_result += f"{forward_file} - Line {line_number}: {line.strip()}\n"

        # Check if forward and backward pointers are at the same position
        if forward_pointer <= backward_pointer:
            # Search for occurrences in the backward file
            backward_file_path = os.path.join(folder_path, backward_file)
            with open(backward_file_path, 'r') as file:
                lines = file.readlines()
                for line_number, line in enumerate(lines, start=1):
                    if re.search(r'\borderId\s{0}\b'.format(order_id), line):
                        backward_result = f"{backward_file} - Line {line_number}: {line.strip()}\n" + backward_result

        forward_pointer += 1
        backward_pointer -= 1

    result = forward_result + backward_result
    return result , start_time

# Example usage:
folder_path = 'blockchain3'
order_id_to_search = 100  # Replace with the orderId you want to search

result , start_time  = search_with_two_pointers(folder_path, order_id_to_search)
t_elapsed = time.time() - start_time
if result:
    print(f"Occurrences of orderId {order_id_to_search} found in the following files:")
    print(result)
    print(f"Time taken : {t_elapsed:.6f}")
else:
    print(f"No occurrences found for orderId {order_id_to_search}.")
