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
