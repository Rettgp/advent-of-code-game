from copy import deepcopy
from itertools import chain


class Location():
    def __init__(self, occupied: bool = False, can_be_occupied: bool = True):
        self.occupied = occupied


class Seating():
    def __init__(self, content: str):
        self.state = dict()
        self.stable = False
        row = 0
        column = 0
        for character in content:
            match (character):
                case 'L':
                    self.state[(row, column)] = False
                    column += 1
                case '#':
                    self.state[(row, column)] = True
                    column += 1
                case '.':
                    column += 1
                case '\n':
                    column = 0
                    row += 1
                case _:
                    pass


    def cycle(self):
        next_state = deepcopy(self.state)
        self.stable = True
        for position, location in next_state.items():
            if location and self.adjacent_occupied_seats(position[0], position[1]) >= 4:
                next_state[(position[0], position[1])] = False
                self.stable = False
            if not location and self.adjacent_occupied_seats(position[0], position[1]) == 0:
                next_state[(position[0], position[1])] = True
                self.stable = False

        self.state = next_state


    def adjacent_occupied_seats(self, row: int, column: int) -> int:
        adjacent_positions = [(-1, -1), (-1, 0), (-1, 1),
                            (0, -1), (0, 1),
                            (1, -1), (1, 0), (1, 1)
                              ]

        adjacent_occupied = 0
        for adjacent_row, adjacent_column in adjacent_positions:
            adjacent_occupied += 1 if self.state.get((adjacent_row + row, adjacent_column + column), False) else 0

        return adjacent_occupied
                
    
    def number_occupied_seats(self):
        return sum([seat for seat in self.state.values()])