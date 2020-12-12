from typing import List
import numpy as np
import sys


class SeatOfLife:
    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix
        self.reset()

    def reset(self):
        self.current_state: np.ndarray = self.matrix.copy()
        self.steps: int = 0

    def tick_adjacent(self):
        """
        Will perform one step of the game applying the rules
        by looking at ADJACENT seats
        :return:
        """

        max_col_idx = self.matrix.shape[1] - 1
        max_row_idx = self.matrix.shape[0] - 1

        new_state = self.current_state.copy()

        # iterate over all seats which are either occupied or empty,
        # hence not a floor (.)
        for relevant_seat in np.argwhere(self.current_state != '.'):
            row, col = relevant_seat

            # we cut a view into the matrix which is like a window
            # around the current position

            # however we have to be aware, that when being on the outermost
            # positions we cannot go further, so we have to limit the windows size
            # according to the maximum extend of the matrix
            window_left = max(0, col - 1)
            window_right = min(col + 1, max_col_idx)

            window_top = max(0, row - 1)
            window_bottom = min(row + 1, max_row_idx)

            window = self.current_state[
                     window_top:window_bottom + 1,
                     window_left:window_right + 1]

            # we do different actions depending if the seat is taken or empty
            is_seat_taken = self.current_state[row, col] == '#'

            if not is_seat_taken:
                is_to_occupy = (window == '#').sum() == 0

                if is_to_occupy:
                    new_state[row, col] = '#'
            else:
                # remember that the current seat we are watching is taken by definition
                # so we have to have at least 5 (not 4) seats within the window taken in order
                # to leave the seat
                is_to_leave = (window == '#').sum() >= 5

                if is_to_leave:
                    new_state[row, col] = 'L'

        self.current_state = new_state
        self.steps += 1

    def tick_view_range(self):
        n_cols = self.matrix.shape[1]
        n_rows = self.matrix.shape[0]

        new_state = self.current_state.copy()

        # iterate over all seats which are either occupied or empty,
        # hence not a floor (.)

        # check west
        for relevant_seat in np.argwhere(self.current_state != '.'):
            row, col = relevant_seat

            visible_west = False
            for i in range(1, col + 1):
                state = self.current_state[row, col - i]
                if state == '.':
                    continue
                else:
                    if state == '#':
                        visible_west = True
                        break
                    else:
                        break

            # check east
            visible_east = False
            for i in range(1, n_cols - col):
                state = self.current_state[row, col + i]
                if state == '.':
                    continue
                else:
                    if state == '#':
                        visible_east = True
                        break
                    else:
                        break

            # check north
            visible_north = False
            for i in range(1, row + 1):
                state = self.current_state[row - i, col]
                if state == '.':
                    continue
                else:
                    if state == '#':
                        visible_north = True
                        break
                    else:
                        break

            # check south
            visible_south = False
            for i in range(1, n_rows - row):
                state = self.current_state[row + i, col]
                if state == '.':
                    continue
                else:
                    if state == '#':
                        visible_south = True
                        break
                    else:
                        break

            # check north-west
            visible_nw = False
            for i in range(1, min(row + 1, col + 1)):
                state = self.current_state[row - i, col - i]
                if state == '.':
                    continue
                else:
                    if state == '#':
                        visible_nw = True
                        break
                    else:
                        break

            # check north-east
            visible_ne = False
            for i in range(1, min(row + 1, n_cols - col)):
                state = self.current_state[row - i, col + i]
                if state == '.':
                    continue
                else:
                    if state == '#':
                        visible_ne = True
                        break
                    else:
                        break

            # check south east
            visible_se = False
            for i in range(1, min(n_cols - col, n_rows - row)):
                state = self.current_state[row + i, col + i]
                if state == '.':
                    continue
                else:
                    if state == '#':
                        visible_se = True
                        break
                    else:
                        break

            # check south west
            visible_sw = False
            for i in range(1, min(col + 1, n_rows - row)):
                state = self.current_state[row + i, col - i]
                if state == '.':
                    continue
                else:
                    if state == '#':
                        visible_sw = True
                        break
                    else:
                        break

            # we do different actions depending if the seat is taken or empty
            is_seat_taken = self.current_state[row, col] == '#'

            sum_seen = int(visible_north) + int(visible_south) + int(visible_east) + int(visible_west) + \
                        int(visible_nw) + int(visible_ne) + int(visible_se) + int(visible_sw)

            if is_seat_taken:
                if sum_seen >= 5:
                    new_state[row, col] = 'L'
            else:
                if sum_seen == 0:
                    new_state[row, col] = '#'


        self.current_state = new_state
        self.steps += 1

    def print_state(self):
        for row_idx in range(self.current_state.shape[0]):
            row = self.current_state[row_idx]
            for col in row:
                print(col, '', end='')

            print('')

    def tick_until_stabilizing(self, mode='adjacent'):
        """
        calls tick until the board doesn't change anymore
        :return:
        """

        while True:
            state_before_tick: np.ndarray = self.current_state.copy()

            if mode == 'adjacent':
                self.tick_adjacent()
            else:
                self.tick_view_range()
            # if all entries are the same, stop
            if (self.current_state == state_before_tick).sum() == self.current_state.shape[0] * self.current_state.shape[1]:
                return


if __name__ == '__main__':
    # read the file
    file_content_lines: List[str]
    with open('input.txt', 'r') as f:
        file_content_lines = f.readlines()

    # split each character in each line so we get a 2d-matrix
    file_content_lines_split: List[List[str]] = [[char for char in line if char != '\n']
                                                 for line in file_content_lines]

    # convert that matrix to a numpy matrix (just for easier handling)
    file_content_matrix: np.ndarray = np.array(file_content_lines_split,
                                               dtype=np.str)

    simulation = SeatOfLife(matrix=file_content_matrix)
    simulation.tick_until_stabilizing()
    simulation.print_state()

    print("End state for adjacent game")
    simulation.print_state()
    n_seats_occupied = (simulation.current_state == '#').sum()
    print("Occupied Seats Adjacent version: ", n_seats_occupied)

    simulation.reset()
    simulation.tick_until_stabilizing('view_range')
    print("End state view range")
    simulation.print_state()
    n_seats_occupied = (simulation.current_state == '#').sum()
    print("Occupied view range version: ", n_seats_occupied)