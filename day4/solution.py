from typing import List, Dict
from functools import reduce
import re


class Passport:
    """
    Represents a read passport
    """
    all_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']

    def __init__(self, data: str):
        # store the (cleaned) plain data
        self.data = data

    def get_entries(self) -> Dict[str, any]:
        return {
            key: value for (key, value) in
            [d.split(':') for d in self.data.split(' ')]
        }

    def keys_available(self, keys: List[str]) -> bool:
        """
        Checks if all [keys] are available in the dictionary
        :param keys:
        :return:
        """

        available_keys = list(self.get_entries().keys())
        return all(key in available_keys for key in keys)

    def check_value_validity(self) -> bool:
        """
        Checks all available keys for complying with the plocy
        :return:
        """
        for key, value in self.get_entries().items():
            if key == 'byr':  # (Birth Year) - four digits; at least 1920 and at most 2002.
                if not (re.match(r'^[0-9]{4}$', value) is not None and 1920 <= int(value) <= 2002):
                    print("Wrong byr", value)
                    return False

            elif key == 'iyr':  # (Issue Year) - four digits; at least 2010 and at most 2020
                if not (re.match(r'^[0-9]{4}$', value) is not None and 2010 <= int(value) <= 2020):
                    print("Wrong iyr", value)
                    return False

            elif key == 'eyr': # (Expiration Year) - four digits; at least 2020 and at most 2030.
                if re.match(r'^[0-9]{4}$', value) is None or not (2020 <= int(value) <= 2030):
                    print("Wrong eyr", value)
                    return False

            elif key == 'hgt':
                # (Height) - a number followed by either cm or in:
                # If cm, the number must be at least 150 and at most 193.
                # If in, the number must be at least 59 and at most 76.

                if len(value) == 5:  # cm
                    if value[-2:] != 'cm':
                        print("Wrong hgt", value)
                        return False
                    val = value[0:3]

                    if not 150 <= int(val) <= 193:
                        print("Wrong hgt", value)
                        return False

                elif len(value) == 4:  # in
                    if value[-2:] != 'in':
                        print("Wrong hgt", value)
                        return False
                    val = value[0:2]
                    if not 59 <= int(val) <= 76:
                        print("Wrong hgt", value)
                        return False
                else:
                    return False

            elif key == 'hcl': # (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
                if not re.match(r'^#[0-9a-f]{6}$', value):
                    print("Wrong hcl", value)
                    return False

            elif key == 'ecl':  # (Eye Color) - exactly one of: amb blu brn gry grn hzl oth
                if value not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                    print("Wrong ecl", value)
                    return False

            elif key == 'pid':
                if not re.match('^[0-9]{9}$', value):
                    print("Wrong ecl", value)
                    return False
            elif key == 'cid':  # we ignore that
                pass
            else:
                print("Wrong key", key)
                return False

        return True


if __name__ == '__main__':

    # (1) read file
    data: List[str]
    with open('input.txt', 'r') as f:
        data = f.readlines()

    # (2) Parse the data
    # we interpret the whole file as a big string, splitting it on '\n\n' (each one is a different entry)
    # and remove the newlines '\n' within all the records
    passports: List[Passport] = [Passport(passport.replace('\n', ' '))
                                 for passport in ''.join(data).split('\n\n')]

    # (3) Task 1: count how many passports are valid by checking if the fields are there
    desired_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    n_valid = reduce(lambda valid_count, passport: valid_count + int(passport.keys_available(desired_fields)),
                     passports,
                     0)

    print("Valid Passports (Task 1): ", n_valid)

    # (4) Task 2: count how many passports are valid by checking if the fields are valid also
    n_valid = reduce(lambda valid_count, passport: valid_count + int(passport.keys_available(desired_fields) and
                                                                     passport.check_value_validity()),
                     passports,
                     0)

    print("Valid Passports (Task 2): ", n_valid)