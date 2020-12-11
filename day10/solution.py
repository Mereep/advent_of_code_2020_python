from typing import List
import math


def count_removables(ordered_adapters: List[int],
                     first_index: int,
                     start: int) -> int:
    """
    This function counts all correct ways of pluging the adapters

    WARNING: This function is very slow and this is likely NOT the best way to do that.
    In fact I didnt even bother to run it through the `input.txt´ file (However, you can verify on the other smaller
    files)

    :param ordered_adapters:
    :param first_index:
    :param start:
    :return:
    """

    if start == len(ordered_adapters) - 1:
        return 1

    if (ordered_adapters[start + 1] - ordered_adapters[first_index]) <= 3:
        wo_score = count_removables(
                                ordered_adapters,
                                start=start + 1,
                                first_index=first_index)

        w_score = count_removables(
                                ordered_adapters,
                                start=start + 1,
                                first_index=start)

        return w_score + wo_score
    else:
        return count_removables(ordered_adapters,
                                start=start + 1,
                                first_index=start)


if __name__ == '__main__':

    # read data
    with open('input.txt', 'r') as f:
        joltages: List[str] = f.readlines()

    # ... and transform numbers to
    joltages_as_numbers = [int(d) for d in joltages]

    # ... sort the numbers in ascending order so we easily can iterate over them
    joltages_as_numbers_sorted = sorted(joltages_as_numbers)

    # count differences of one and 3 jolts between subsequent joltages (Task I)
    n_differences_of_3 = 0
    n_differences_of_1 = 0

    # add the "voltage" of 0 before everything (simulates input)
    joltages_as_numbers_sorted.insert(0, 0)

    # and add a an entry of value `max + 3´ for the very last output (simulates output)
    joltages_as_numbers_sorted.append(joltages_as_numbers_sorted[-1] + 3)

    for index in range(1, len(joltages_as_numbers_sorted)):
        difference = joltages_as_numbers_sorted[index] - joltages_as_numbers_sorted[index - 1]
        if difference == 3:
            n_differences_of_3 += 1
        elif difference == 1:
            n_differences_of_1 += 1
        elif difference == 2:
            break       # This case is not of interest
        elif difference > 3:
            raise Exception("There can only be differences of max 3 jolts (Code: 938129)")

    print("1 jolt differences: ", n_differences_of_1)
    print("3 jolt differences: ", n_differences_of_3)
    print("multiplication of those: ", n_differences_of_3 * n_differences_of_1)

    # Part II: Count all valid ways to plug the adapters together (keeping the final valid output)
    # remember that each time we `could´ remove on adapter from the chain that
    # would be a valid permutation

    # 0 1 2 3 4 5 6           4 5 6 8 9 10 13 14 17
    # Max: n2^(len(adapters)) ways that could be theoretical checked
    # --> most of them can NEVER be valid

    # count "removable" adapters
    n_removable_single = count_removables(joltages_as_numbers_sorted, first_index=0, start=1)

    print(n_removable_single)




