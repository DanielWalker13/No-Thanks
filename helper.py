"""General support functions for the application."""

from collections import Counter


def rotate_list_order(lst, item):
    """Rotate the order of the lsts."""
    try:
        # Find the index of the given value
        index = lst.index(item)
        # Rotate the list so that the specified value comes first
        return lst[index:] + lst[:index]
    except ValueError:
        # UPGRADE: Handle error
        # Value not found in the list, return the list as is or handle the error as needed
        return lst


# TODO: Have chate gpt breakdown this code to analyze
def remove_sequential_numbers(numbers):
    """Remove sequential numbers from a list of numbers."""
    if not numbers:
        return [], []

    non_seq_num = []
    seq_num = []

    num = 0
    while num < len(numbers):
        non_seq_num.append(numbers[num])
        current_num = num  # Initialize sequence end to the current index

        # Look ahead to find the end of the sequence
        while (
            current_num + 1 < len(numbers)
            and numbers[current_num] + 1 == numbers[current_num + 1]
        ):
            current_num += 1

        if num != current_num:
            seq_num.extend(
                numbers[num + 1 : current_num + 1]
            )  # Exclude the first number of the sequence

        num = current_num + 1  # Increment

    return non_seq_num, seq_num


def identify_dupes(ls: list) -> set[int]:
    counter = Counter(ls)
    duplicates = {num for num, count in counter.items() if count > 1}
    return duplicates
