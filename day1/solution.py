from typing import List, Tuple


def first_solution(sorted_numbers: List[int]) -> [int, int]:
    """
    Iterate over all pairs of numbers returning two numbers summing to 2000

    returns that pair
    :param sorted_numbers:
    :return:
    """
    # (3) iterate over all PAIRS of sorted numbers
    for first_number_index in range(len(sorted_numbers) - 1):
        for second_number_index in range(first_number_index + 1, len(sorted_numbers)):
            first_number = sorted_numbers[first_number_index]
            second_number = sorted_numbers[second_number_index]

            # (3.1) Check sum of numbers
            number_sum = first_number + second_number

            # (3.2) break if the sum is already over 2000
            # since the numbers are sorted it is impossible to find a valid pair later
            if number_sum > 2020:
                break

            if number_sum == 2020:
                return first_number, second_number

def second_solution(sorted_numbers: List[int]) -> [int, int, int]:
    """
    Iterate over all TRIPLETS of numbers returning two numbers summing to 2000

    returns that triplet
    (basically the same as first_solution)
    :param sorted_numbers:
    :return:
    """
    # (3) iterate over all PAIRS of sorted numbers
    for first_number_index in range(len(sorted_numbers) - 2):
        for second_number_index in range(first_number_index + 1, len(sorted_numbers)):
            for third_number_index in range(second_number_index + 1, len(sorted_numbers)):
                first_number = sorted_numbers[first_number_index]
                second_number = sorted_numbers[second_number_index]
                third_number = sorted_numbers[third_number_index]

                # (3.1) Check sum of numbers
                number_sum = first_number + second_number + third_number

                # (3.2) break if the sum is already over 2000
                # since the numbers are sorted it is impossible to find a valid pair later
                if number_sum > 2020:
                    break

                if number_sum == 2020:
                    return first_number, second_number, third_number


if __name__ == '__main__':
    # (1) read file
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    numbers: List[int] = [int(line) for line in lines]

    # (2) sort them by size (ascending order per default)
    sorted_numbers = sorted(numbers)

    # First solution (PAIRS) of numbers
    first_number, second_number = first_solution(sorted_numbers)

    print("First result:")
    print(f"Found result with {first_number} and {second_number}. "
          f"Product ist: {first_number * second_number}")

    # Second solution TRIPLETS of numbers
    first_number, second_number, third_number = second_solution(sorted_numbers)

    print("First result:")
    print(f"Found result with {first_number}, {second_number}, {third_number} "
          f"Product ist: {first_number * second_number * third_number}")
