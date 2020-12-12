from typing import List, Optional


class Position:

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y


class Ship:
    def __init__(self):
        self.ship_angle: int = 270
        self.ship_position: Position = Position()
        self.waypoint_position: Position = Position(x=10, y=1)

    def get_ship_facing(self) -> str:
        """
        Turns the degrees into an readable string
        :return:
        """
        if self.ship_angle == 270:
            return 'E'
        elif self.ship_angle == 0:
            return 'N'
        elif self.ship_angle == 90:
            return 'W'
        elif self.ship_angle == 180:
            return 'S'
        else:
            raise Exception(f"Illegal state {self.ship_angle} degrees")

    def move_ship(self, instruction: str):
        """
        Executes one command / instruction with target ship (Task I)
        :param instruction:
        :return:
        """

        movement: str = instruction[0]
        distance: int = int(instruction[1:])

        if movement == 'N':  # move north
            self.ship_position.y += distance
        elif movement == 'S':  # move south
            self.ship_position.y -= distance
        elif movement == 'E':  # move east
            self.ship_position.x += distance
        elif movement == 'W':  # move west
            self.ship_position.x -= distance
        elif movement == 'F':  # move in direction the ship is 'F'acing to (Forward)
            facing: str = self.get_ship_facing()
            return self.move_ship(f"{facing}{distance}")
        elif movement == 'R':   # turn the ship to the right
            self.ship_angle = (self.ship_angle - distance) % 360
        elif movement == 'L':   # turn the ship tp the left
            self.ship_angle = (self.ship_angle + distance) % 360
        else:
            raise Exception(f"Illegal movement instruction {instruction}")

    def move_waypoint(self, instruction: str):
        """
        Executes one command / instruction with target waypoint (Task II)
        :param instruction:
        :return:
        """

        movement: str = instruction[0]
        distance: int = int(instruction[1:])

        print(movement, distance)
        if movement == 'N':  # move north
            self.waypoint_position.y += distance
        elif movement == 'S':  # move south
            self.waypoint_position.y -= distance
        elif movement == 'E':  # move east
            self.waypoint_position.x += distance
        elif movement == 'W':  # move west
            self.waypoint_position.x -= distance
        elif movement == 'F':  # move in direction the ship is 'F'acing to (Forward)
            east_west_movement = self.waypoint_position.x * distance
            north_south_movement = self.waypoint_position.y * distance
            self.move_ship(f"E{east_west_movement}")
            self.move_ship(f"N{north_south_movement}")

        elif movement == 'R':   # turn the ship to the right
            curr_x = self.waypoint_position.x
            curr_y = self.waypoint_position.y

            if distance == 90:
                self.waypoint_position.y = -curr_x
                self.waypoint_position.x = curr_y
            elif distance == 180:
                self.waypoint_position.y = -self.waypoint_position.y
                self.waypoint_position.x = -self.waypoint_position.x
            elif distance == 270:
                self.waypoint_position.y = curr_x
                self.waypoint_position.x = -curr_y
            else:
                raise Exception(f"Illegal turn angle R{distance}")

        elif movement == 'L':   # turn the ship tp the left
            return self.move_waypoint(f'R{360-distance}')


if __name__ == '__main__':
    file_contents: List[str]

    with open('input.txt', 'r') as f:
        file_contents = f.readlines()

    ship: Ship = Ship()

    for instruction in file_contents:
        ship.move_ship(instruction)

    print("Mode Ship movement")
    print(f"Distance eastwest: {ship.ship_position.x}\nDistance nothsouth: {ship.ship_position.y}\n\n"
          f"Manhatten Distance: {abs(ship.ship_position.x) + abs(ship.ship_position.y)}")

    print("\n\n\nMode Waypoint movemenet")
    ship2: Ship = Ship()

    for instruction in file_contents:
        ship2.move_waypoint(instruction)

    print(f"Distance eastwest: {ship2.ship_position.x}\nDistance nothsouth: {ship2.ship_position.y}\n\n"
          f"Manhatten Distance: {abs(ship2.ship_position.x) + abs(ship2.ship_position.y)}")