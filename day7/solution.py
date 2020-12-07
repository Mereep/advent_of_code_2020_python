from typing import List, Dict, Set, Tuple


def load_data_structure(file_name: str) -> Dict[str, List[Tuple[int, str]]]:
    """
    Reads the included `input.txt´ file
    and returns a data structure containing a lookup in the form of `color_name => (amount, child_color_name)´

    :param file_name:
    :return:
    """
    bags: Dict[str, List[Tuple[int, str]]] = {}

    with open(file_name, 'r') as f:
        lines: List[str] = f.readlines()

    for line in lines:
        bag_name, content = line.split('contain')
        bag_name = bag_name[:-6]

        bag_contents = [c.strip()
                        for c in content.split(',')]

        inside_bags = []
        for bag_content in bag_contents:
            # print(bag_content)
            content_parts = bag_content.split(' ')
            inside_bag_name = ' '.join(content_parts[1:3])
            if content_parts[0] == 'no':
                pass
            else:
                amount = int(content_parts[0])
                inside_bags.append((amount, inside_bag_name))

        bags[bag_name] = inside_bags

    return bags


def count_ways_from_to(from_color: str,
                       to_color: str,
                       graph: Dict[str, List[Tuple[int, str]]],
                       ) -> int:
    """
    Count all possible ways from a given `from_color´ to the `to_color´

    :param from_color:
    :param to_color:
    :param graph:
    :return:
    """
    n_inside = 0
    for child in graph[from_color]:
        n_childs, child_color = child
        if child_color == to_color:
            n_inside += 1

        n_inside += count_ways_from_to(
                                  child_color,
                                  to_color,
                                  graph)

    return n_inside


def expand_to(color_from: str, end_to: str,
              data: Dict[str, List[Tuple[int, str]]],
              to_golden: Set[str],
              path: List[str]):
    """
    Finds a way from color_from to end_color in graph `data´ (Task 1)

    :param color_from:
    :param end_to:
    :param data:
    :param to_golden: which colors have a known way to golden (will be kept track of)
    :param path: current path beginning from color_from
    :return:
    """
    # expanded.add(color_from)
    path.append(color_from)

    for child in data[color_from]:
        amount, curr_color = child

        if curr_color == end_to:
            to_golden.update(path)
        else:
            expand_to(curr_color,
                      end_to,
                      data,
                      to_golden,
                      path.copy())


def count_total_bag_sum(color_from: str,
                        data: Dict[str, List[Tuple[int, str]]]) -> int:
    """
    Counts amount of bags beginning from color_from (Task 2)

    the graph is expected to have NO CYCLES
    :param color_from:
    :param data:
    :return:
    """
    current_sum = 0
    for child in data[color_from]:
        amount, color = child
        current_sum += amount * (1 + count_total_bag_sum(color, data))

    return current_sum


if __name__ == '__main__':
    graph = load_data_structure('input.txt')

    all_colors = []
    for data in graph.values():
        all_colors += [d[1] for d in data]

    all_colors += [*graph.keys()]

    to_golden = set()

    for color in set(all_colors):
        expand_to(color, 'shiny gold', graph, to_golden, [])

    print("ways to gold", len(to_golden))
    print("weight of gold", count_total_bag_sum('shiny gold', graph))