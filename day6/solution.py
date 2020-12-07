from typing import List, Set


class Group:
    """
    Collects all answers of a specific group
    where each group member has one line of letters as `azghf´ each indicating a positive answer
    """
    def __init__(self, answers: List[str]):
        # plain data (source)
        self.answers = answers

    def get_all_possible_answers(self) -> Set[str]:
        """
        Gets a set of all letters that popup within ANY group member

        (just for warmup; not needed)
        :return:
        """
        possible_answers: Set[str] = set()

        for person_answers in self.answers:
            for answer in person_answers:
                possible_answers.add(answer)

        return possible_answers

    def answers_whole_group_positive(self) -> Set[str]:
        """
        answers (letters) which where found within ALL members

        :return:
        """

        all_true: Set[str] = set(self.answers[0])

        if self.n_members() > 1:
            for person_answers in self.answers[1:]:
                all_true = all_true.intersection(set(person_answers))

        return all_true

    def count_answers_whole_group_positive(self) -> int:
        """
        counts [answers_whole_group_positive]
        :return:
        """
        return len(self.answers_whole_group_positive())

    def answers_any_member_positive(self) -> Set[str]:
        """
        answers (letters) which where found within SOME (at least one) members

        :return:
        """
        any_true: Set[str] = set()
        for person_answers in self.answers:
            any_true.update(person_answers)

        return any_true

    def count_answers_any_member_positive(self) -> int:
        """
        counts [answers_any_member_positive]
        :return:
        """
        return len(self.answers_any_member_positive())

    def n_members(self) -> int:
        return len(self.answers)


if __name__ == "__main__":

    # (i) read file (all lines as separate list entry)
    with open("input.txt", "r") as f:
        group_lines: List[str] = []
        all_lines = f.readlines()

    # (ii) create groups (they are separated by an empty line)
    groups: List[Group] = []
    for line in all_lines:
        line = line.strip() # just remove some trailing fun
        if line != "":
            group_lines.append(line)
        else:
            groups.append(Group(group_lines))
            group_lines = []

    # dont forget the last entry
    groups.append(Group(group_lines))

    # (iii) some tests
    print("Some debug info")
    print(
        groups[-1].answers, "\n"
        "All positives", groups[-1].answers_whole_group_positive(), groups[-1].count_answers_whole_group_positive(), "\n"
        "Any positives", groups[-1].answers_any_member_positive(), groups[-1].count_answers_any_member_positive(), "\n")


    # second quest: sum of answers any group member was positive about
    sum_of_anyone_positive = 0

    # second quest: sum of answers each (all of them) group member was positive about
    sum_of_everyone_positive = 0
    for group in groups:
        sum_of_anyone_positive += group.count_answers_any_member_positive()
        sum_of_everyone_positive += group.count_answers_whole_group_positive()

    print("# answers ANYONE answered positive over all groups: ", sum_of_anyone_positive)
    print("# answers EVERYONE positive over all groups: ", sum_of_everyone_positive)