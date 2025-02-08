import os
import shutil
import heapq
import time


def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s


def read_audio_files(file_path):
    audio_files = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                print(f"Warning: Skipping empty line at {line_number}")
                continue
            try:
                filename, duration = line.split(" ")
                duration_in_seconds = time_to_seconds(duration)
                audio_files.append((filename, duration_in_seconds))
            except ValueError:
                print(f"Error: Invalid format on line {line_number}: {line}")
                continue
    return audio_files


# fatma
def optimized_first_fit_decreasing_heap(files, folder_capacity):
    folders = []
    folder_capacities = []

    for file_size in files:
        filename, file_size_value = file_size  # Extract the actual file size value
        if file_size_value > folder_capacity:
            return None

        if not folder_capacities:
            folders.append([file_size])
            heapq.heappush(folder_capacities, (-folder_capacity + file_size_value, len(folders) - 1))
            continue

        min_remaining_capacity, min_index = folder_capacities[0]  # Correct extraction

        if file_size_value <= -min_remaining_capacity:  # Correct Comparison
            heapq.heapreplace(folder_capacities, (min_remaining_capacity + file_size_value, min_index))
            folders[min_index].append(file_size)
        else:
            folders.append([file_size])
            heapq.heappush(folder_capacities, (-folder_capacity + file_size_value, len(folders) - 1))

    return folders


def best_fit_sound_files_exact_capacity_heap(files, folder_capacity):
    folders = []
    folder_capacities = []

    for file_size in files:
        if file_size > folder_capacity:
            return None

        best_fit_index = None

        possible_folders = []
        while folder_capacities and file_size <= -folder_capacities[0][0]:  # Correct Comparison
            possible_folders.append(heapq.heappop(folder_capacities))

        if possible_folders:
            best_fit_index = possible_folders[-1][1]

        for folder_capacity_tuple in possible_folders:
            heapq.heappush(folder_capacities, folder_capacity_tuple)

        if best_fit_index is not None:
            remaining_capacity = - \
            heapq.heapreplace(folder_capacities, (folder_capacities[0][0] + file_size, best_fit_index))[0]
            folders[best_fit_index].append(file_size)
        elif file_size <= folder_capacity:
            folders.append([file_size])
            heapq.heappush(folder_capacities, (-folder_capacity + file_size, len(folders) - 1))
        else:
            return None

    return folders


# medany

def allocate_with_worst_fit(audio_files, folder_capacity):
    folders = []
    heap = []  # Priority queue (min-heap) storing (remaining_capacity, folder_index)

    # Sort files in decreasing order of duration (same as First Fit Decreasing)
    sorted_audio_files = sorted(audio_files, key=lambda x: x[1], reverse=True)

    for file, duration in sorted_audio_files:  # Unpack each file and duration
        placed = False

        # Check if there's a folder that can accommodate the file
        if heap:
            # Look for the folder with the maximum remaining capacity
            remaining_capacity, folder_index = heapq.heappop(heap)
            remaining_capacity = -remaining_capacity  # Convert back to positive value

            if remaining_capacity >= duration:
                # Place file in this folder
                folders[folder_index].append((file, duration))
                remaining_capacity -= duration
                heapq.heappush(heap, (-remaining_capacity, folder_index))  # Push updated folder back to the heap
                placed = True
            else:
                # Push it back as it couldn't fit
                heapq.heappush(heap, (-remaining_capacity, folder_index))

        # If not placed, create a new folder
        if not placed:
            new_folder_index = len(folders)
            folders.append([(file, duration)])  # Start a new folder with this file
            remaining_capacity = folder_capacity - duration
            heapq.heappush(heap, (-remaining_capacity, new_folder_index))  # Push new folder to the heap

    return folders


# ali

def dynamic_programming_folder_filling(files, folder_capacity):
    folders = []

    while files:
        # Sort files by duration in descending order
        files.sort(key=lambda x: x[1], reverse=True)
        n = len(files)
        durations = [file[1] for file in files]  # Extract durations
        dp = [[0] * (folder_capacity + 1) for _ in range(n + 1)]

        # Build DP table
        for i in range(1, n + 1):
            for j in range(1, folder_capacity + 1):
                if durations[i - 1] <= j:
                    dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - durations[i - 1]] + durations[i - 1])
                else:
                    dp[i][j] = dp[i - 1][j]

        # Retrieve the selected files
        selected_files = []
        capacity = folder_capacity
        for i in range(n, 0, -1):
            if dp[i][capacity] != dp[i - 1][capacity]:
                selected_files.append(files[i - 1])
                capacity -= durations[i - 1]

        folders.append(selected_files)

        for file in selected_files:
            files.remove(file)

    return folders


# mahmoud
def worst_fit_decreasing_linear(audio_files, time_capacity):
    # Sort audio files by duration in descending order
    audio_files.sort(key=lambda x: x[1], reverse=True)  # O(n log n)

    folders = []  # O(1)
    folder_remaining_time = []  # O(1)

    # Total Complexity: O(n * m), where n is the number of audio files, and m is the number of folders
    for file, duration in audio_files:  # O(n), loop through each audio file
        worst_fit_index = -1  # O(1)
        max_remaining_time = -1  # O(1)

        # Find the folder with the most remaining space that can fit the file
        for i in range(len(folders)):  # O(m), where m is the number of folders
            if folder_remaining_time[i] >= duration and folder_remaining_time[i] > max_remaining_time:  # O(1)
                max_remaining_time = folder_remaining_time[i]  # O(1)
                worst_fit_index = i  # O(1)

        if worst_fit_index != -1:  # O(1)
            # Place the file in the worst-fit folder
            folders[worst_fit_index].append((file, duration))  # O(1), append file to the folder
            folder_remaining_time[worst_fit_index] -= duration  # O(1), update remaining capacity
        else:
            # Create a new folder if no folder is suitable for the file
            folders.append([(file, duration)])  # O(1), add a new folder
            folder_remaining_time.append(time_capacity - duration)  # O(1), track new folder's remaining capacity

    return folders  # O(1)


# Overall Complexity:
# Sorting: O(n log n)
# Outer Loop: O(n)
# Inner Loop (Finding worst fit): O(m), where m is the number of folders
# Total Outer-Inner Complexity: O(n * m)
# Overall: O(n log n + n * m)
# Worst-case complexity: O(n log n + n^2), when every file creates a new folder.
# Approach: Greedy

# mohamed
def worst_fit_linear_search(files, folder_capacity):
    """
    Organize files into folders using the Worst-fit algorithm.
    Returns a list of lists, where each inner list contains the files in a folder.
    """
    folders = []  # List to store files in each folder
    folder_capacities = []  # List to track remaining capacities of folders

    for file_name, duration in files:
        max_remaining = -1
        best_folder_index = -1

        # Find the folder with the maximum remaining capacity
        for i, remaining_capacity in enumerate(folder_capacities):
            if remaining_capacity >= duration and remaining_capacity > max_remaining:
                max_remaining = remaining_capacity
                best_folder_index = i

        if best_folder_index == -1:
            # Create a new folder if no suitable one exists
            folders.append([(file_name, duration)])
            folder_capacities.append(folder_capacity - duration)
        else:
            # Add the file to the best folder
            folders[best_folder_index].append((file_name, duration))
            folder_capacities[best_folder_index] -= duration

    return folders


def save_folders_to_files(folders, destination_dir):
    output_dir = destination_dir
    os.makedirs(output_dir, exist_ok=True)

    for i, folder in enumerate(folders, start=1):
        folder_name = os.path.join(output_dir, f"folder_{i}.txt")
        with open(folder_name, 'w') as f:
            total_duration = sum(file[1] for file in folder)  # Optimize by tracking this earlier
            f.write(f"Total Duration: {total_duration} seconds\n")
            f.write("Files:\n")
            for file in folder:
                f.write(f"{file[0]} - {file[1]} seconds\n")


def create_folders_and_copy_files(source_directory, packed_folders, destination_directory):
    for folder_idx, folder_files in enumerate(packed_folders, start=1):
        # make folders to move to
        folder_name = os.path.join(destination_directory, f"Folder_{folder_idx}")
        os.makedirs(folder_name, exist_ok=True)
        print(f"Created folder: {folder_name}")

        # Copy files into the folder
        for file, duration in folder_files:
            src = os.path.join(source_directory, file)
            dst = os.path.join(folder_name, file)
            if os.path.exists(src):
                shutil.copy(src, dst)
                print(f"Copied: {file} ({duration} seconds) -> {folder_name}")
            else:
                print(f"Warning: File {file} not found in source directory!")


def switch_case_algorithm(choice, audio_files, folder_capacity):
    algorithms = {
        "optimized_first_fit": optimized_first_fit_decreasing_heap,
        "worst_fit_heap": allocate_with_worst_fit,
        "dynamic_programming": dynamic_programming_folder_filling,
        "worst_fit_decreasing_linear": worst_fit_decreasing_linear,
        "worst_fit_linear_search": worst_fit_linear_search,
        "best_fit": best_fit_sound_files_exact_capacity_heap
    }

    if choice in algorithms:
        return algorithms[choice](audio_files, folder_capacity)
    else:
        raise ValueError(f"Invalid choice: {choice}. Available options are: {', '.join(algorithms.keys())}")


def clear_output_directory(output_dir):
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Delete the file

                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Delete the directory
                    print(f"Deleted directory: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    else:
        os.makedirs(output_dir)
        print(f"Output directory created: {output_dir}")


def main():
    input_file = r"D:\Downloads\Complete1\Complete1\AudiosInfo.txt"
    source_dir = r"D:\Downloads\Complete1\Complete1\Audios"
    destination_dir = r"D:\Projects\Algo test"
    folder_capacity = 100

    clear_output_directory(destination_dir)
    audio_files = read_audio_files(input_file)

    print("Choose an algorithm:")
    print("1. Optimized First Fit Decreasing")
    print("2. Worst Fit Heap")
    print("3. Dynamic Programming Folder Filling")
    print("4. Worst Fit Decreasing Linear")
    print("5. Worst Fit Linear Search")
    print("6. Best Fit")

    choice = input("Enter the number corresponding to your choice: ")

    mapping = {
        "1": "optimized_first_fit",  # Optimized First Fit Decreasing
        "2": "worst_fit_heap",  # Allocate With Worst Fit (Heap Implementation)
        "3": "dynamic_programming",  # Dynamic Programming Folder Filling
        "4": "worst_fit_decreasing_linear",  # Corrected: Mapping to worst_fit_decreasing_linear
        "5": "worst_fit_linear_search",  # Worst Fit Linear Search
        "6": "best_fit"  # Best Fit Optimized
    }

    start_time = time.time()
    selected_algorithm = mapping.get(choice)

    if not selected_algorithm:
        print("Invalid choice. Exiting...")
        return

    packed_folders = switch_case_algorithm(selected_algorithm, audio_files, folder_capacity)

    save_folders_to_files(packed_folders, destination_dir)
    create_folders_and_copy_files(source_dir, packed_folders, destination_dir)
    end_time = time.time()
    total_time_seconds = (end_time - start_time)
    print(f"Total execution time: {total_time_seconds:.2f} sec")


if __name__ == "__main__":
    main()
