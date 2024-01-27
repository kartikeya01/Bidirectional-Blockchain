import os
import time

def search_order_id_in_files(folder_path, order_id):
    occurrences = []

    # Get a list of files in the specified folder
    file_list = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    # Iterate over files in the order they are stored in the folder
    file_list.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    start_time = time.time()
    for filename in file_list:
        file_path = os.path.join(folder_path, filename)
        
        # Open the file and search for occurrences
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

# Example usage:
folder_path = 'blockchain3'
order_id_to_search = 100  # Replace with the exact orderId you want to search

result ,start_time= search_order_id_in_files(folder_path, order_id_to_search)
t_elapsed = time.time() - start_time

if result:
    print(f"Occurrences of orderId {order_id_to_search} found in the following files:")
    for occurrence in result:
        print(f"{occurrence['file']} - Line {occurrence['line_number']}: {occurrence['line']}")
    print(f"Time taken : {t_elapsed:.6f}")
else:
    print(f"No occurrences found for orderId {order_id_to_search}.")
