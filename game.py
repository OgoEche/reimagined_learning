# Write your code here
class KnightPuzzle:
    def __init__(self):
        # self.matrix = [[(x, y) for x in range(1, size + 1)] for y in range(size, 0, -1)]
        self.matrix = None
        self.prompt = {"dim_msg": "Enter your board dimensions: > ",
                       "pos_msg": "Enter the knight's starting position: > ",
                       "nex_msg": "Enter your next move: > ",
                       "que_msg": "Do you want to try the puzzle? (y/n): > "}

        self.error = {"dim_err": "Invalid dimensions!",
                      "pos_err": "Invalid position!",
                      "nex_err": "Invalid move!",
                      "nex_not": "No more possible moves!",
                      "que_err": "Invalid input!"}
        self.cell_size = None  # is the length of a placeholder for one cell
        self.border_length = None
        self.x_column_n = None  # is the number of columns
        self.y_row_n = None
        self.current_position = []
        self.possible_moves_from_position = []
        self.backtrack_position = {}
        # build a list of all knight's movements. Initially nested but then flattened
        self._nested = [[(x, y) for x in range(-2, 3) if x != 0 and abs(x) != abs(y)] for y in range(-2, 3) if y != 0]
        self.knight_movements = [item for sublist in self._nested for item in sublist]  # flatten list

    def build_matrix(self, x_cols, y_rows):
        self.x_column_n = x_cols
        self.y_row_n = y_rows
        self.cell_size = len(str(x_cols * y_rows))
        self.matrix = [['_'*self.cell_size for x in range(x_cols)] for y in range(y_rows)]
        self.calc_border_length()

    def calc_border_length(self):
        self.border_length = self.x_column_n * (self.cell_size + 1) + 3

    def display_matrix(self, _update_with_val=None):

        # when you need to reflect all possible moves from a given position
        # _update_with_val: will hold the possible moves
        if _update_with_val:
            for corr, val in _update_with_val:
                self.set_position(*corr, val)

        print(f"{' ' * (self.cell_size - 1)}{'-' * self.border_length}")
        for idx, val in enumerate(self.matrix, 0):
            print(f'{len(self.matrix) - idx:<{self.cell_size-1}}| {" ".join(val)} |')
        print(f"{' ' * (self.cell_size - 1)}{'-' * self.border_length}")
        print(f"{' ' * (1 + self.cell_size)}{' '.join([' '*(len(v) - len(str(i))) + str(i) for i, v in enumerate(val, 1)])}")
        
        self.flush_possible_movement_from_matrix()

    def get_user_input(self, input_prompt, error_msg, input_type=None):
        raw_input = input(f"{input_prompt}").split(' ')
        return self.check_user_input(raw_input, error_msg, input_type)

    def check_user_input(self, raw_user_input, error_msg, input_type):
        if input_type == 'que' and raw_user_input[-1] not in ['y', 'n', ' ']:
            print(f"{error_msg}")
            return 'Invalid'
        if input_type != 'que' and not all(x.isnumeric() for x in raw_user_input):
            print(f"{error_msg}")
            return 'Invalid'
        if input_type != 'que' and len(raw_user_input) != 2:
            print(f"{error_msg}")
            return 'Invalid'
        if input_type != 'que' and any(int(x) < 1 for x in raw_user_input):
            print(f"{error_msg}")
            return 'Invalid'
        if input_type == 'pos' and int(raw_user_input[0]) > self.x_column_n and int(raw_user_input[1]) > self.y_row_n:
            print(f"{error_msg}")
            return 'Invalid'
        if input_type == 'nex' and ([int(v) for v in raw_user_input] in self.current_position or
                                    not self.is_valid_move([int(v) for v in raw_user_input])):
            print(f"{error_msg}", end=' ')
            return 'Invalid', raw_user_input

        return [int(v) for v in raw_user_input] if input_type != 'que' else raw_user_input

    def reset_and_move_position(self, x_col, y_row, backtrack=False):
        # get current position and reset with placeholder for visited square with *
        x_col_current, y_row_current = self.current_position[-1]
        if backtrack:
            self.matrix[-y_row_current][x_col_current - 1] = f"{' ' * (self.cell_size - 1)}X"
            self.matrix[-y_row][x_col - 1] = '_' * self.cell_size
        else:
            self.matrix[-y_row_current][x_col_current - 1] = f"{' ' * (self.cell_size - 1)}*"
            # move to next possible position and update current position
            self.set_current_position(x_col, y_row)

    def set_current_position(self, x_col, y_row, postfix='X'):
        self.current_position.append([x_col, y_row])
        self.set_position(x_col, y_row)

    def set_position(self, x_col, y_row, postfix='X'):
        # self.matrix[-position[-1]][position[0] - 1] = 'X'
        # self.current_position = [x_col, y_row]
        self.matrix[-y_row][x_col - 1] = f"{' ' * (self.cell_size - 1)}{postfix}" if len(str(postfix)) == 1 else f"{postfix}"

    def label_visited_squares(self):
        for idx, val in enumerate(self.current_position, 1):
            self.set_position(*val, postfix=idx)

    def is_valid_move(self, possible_position):
        # start from current position to determine moves and then check whether possible_position is valid
        move = [[sum(x) for x in zip(self.current_position[-1], y)] for y in self.knight_movements]
        _possible_movements = [val for val in move if self.x_column_n >= val[0] > 0 and self.y_row_n >= val[1] > 0
                               and val not in self.current_position]
        return possible_position in _possible_movements

    def is_move_possible(self, possible_position):
        # Get all possible movement before filtering ones outside the matrix boundary
        # Also filtering already visited squares
        move = [[sum(x) for x in zip(possible_position, y)] for y in self.knight_movements]
        _possible_movements = [val for val in move if self.x_column_n >= val[0] > 0 and self.y_row_n >= val[1] > 0
                               and val not in self.current_position]

        #return False if _possible_movements else True
        if _possible_movements:
            return False
        else:
            print()
            print(self.error['nex_not'])
            print(f'Your knight visited {len(self.current_position)} squares!')
            return True

    def is_all_square_visited(self):
        # more of, go through the matrix and check that it's only X and * left or just the placeholder
        placeholder = '_'*self.cell_size
        remainder = [item for sublist in self.matrix for item in sublist if placeholder == item]
        return False if remainder else True

    def flush_possible_movement_from_matrix(self, from_start=False):
        # more of, go through the matrix and reset cells with placeholder except those with X and *
        # except for when we want to reset from the start
        marked_position_symbol = f"{' ' * (self.cell_size - 1)}X"
        marked_visited_sq_symbol = f"{' ' * (self.cell_size - 1)}*"
        placeholder = '_' * self.cell_size
        if from_start:
            self.current_position = [self.current_position[0]]
            self.matrix = [[placeholder for val in sublist] for sublist in self.matrix]
            self.set_position(*self.current_position[-1])
            return

        marker = marked_position_symbol, marked_visited_sq_symbol
        self.matrix = [[val if val in marker else placeholder for val in sublist] for sublist in self.matrix]

    def is_possible_solution(self, _current_position, dest=True):

        # base case 1: if solution to puzzle
        if self.is_all_square_visited():
            return True
        else:
            # sort by number of possible moves from a landing position and pop one with the least possible moves count
            _possible_moves = sorted(self.get_possible_movement(_current_position), key=lambda ct: ct[-1], reverse=dest)
            if _possible_moves and not self.is_all_square_visited():
                position, number_of_moves = _possible_moves.pop()
                self.reset_and_move_position(*position)
                return self.is_possible_solution(position)
            else:
                # if we hit a dead end, get previous position, reverse and pick moves with the highest possible count.
                prev_position = self.current_position.pop()
                self.reset_and_move_position(*prev_position, backtrack=True)
                self.backtrack_position[tuple(prev_position)] = self.backtrack_position.get(tuple(prev_position), 0) + 1
                # base case 2:  if no solution to puzzle, where a position repeats in backtrack
                if self.backtrack_position[tuple(prev_position)] > 1:
                    return False
                return self.is_possible_solution(self.current_position[-1], dest=False)

    def get_possible_movement(self, possible_position, _monitor_list=None):
        # Get all possible movement before filtering ones outside the matrix boundary
        # Also filtering already visited squares
        move = [[sum(x) for x in zip(possible_position, y)] for y in self.knight_movements]
        _possible_movements = [val for val in move if self.x_column_n >= val[0] > 0 and self.y_row_n >= val[1] > 0
                               and val not in self.current_position]
        # starting point - hold the initial lists of movements from the starting point
        if _monitor_list is None:
            _monitor_list = list(_possible_movements)
            self.possible_moves_from_position = []

        # update matrix position
        if self.current_position[-1] == list(possible_position):
            self.set_position(*possible_position)
        else:
            # self.set_position(*possible_position, len(_possible_movements))
            self.possible_moves_from_position.append((tuple(possible_position), len(_possible_movements)))

        # base case - empty initial list of possible movements from starting position
        if not _monitor_list:
            return self.possible_moves_from_position
        # recursive step - to check other possible movements and their count
        next_position = _monitor_list.pop()
        return self.get_possible_movement(next_position, _monitor_list)

    def main_processing(self):
        # prompt for dimensions, build board and calculate border length
        while user_response := self.get_user_input(self.prompt['dim_msg'], self.error['dim_err']):
            if user_response != 'Invalid':
                self.build_matrix(*user_response)
                break
        # prompt for starting position and update board
        while user_response := self.get_user_input(self.prompt['pos_msg'], self.error['pos_err'], input_type='pos'):
            if user_response != 'Invalid':
                self.set_current_position(*user_response)
                #possible_moves = self.get_possible_movement(user_response)
                #self.display_matrix(possible_moves)
                break
        # prompts user on whether they want to try the puzzle or not or see the line solution
        while user_response := self.get_user_input(self.prompt['que_msg'], self.error['que_err'], input_type='que'):
            if user_response != 'Invalid' and user_response[-1] == 'y':
                if not self.is_possible_solution(self.current_position[-1]):
                    print('No solution exists!')
                    return
                else:
                    self.flush_possible_movement_from_matrix(from_start=True)
                    possible_moves = self.get_possible_movement(self.current_position[-1])
                    self.display_matrix(possible_moves)
                    break
            elif user_response != 'Invalid' and user_response[-1] == 'n':
                if self.is_possible_solution(self.current_position[-1]):
                    self.label_visited_squares()
                    print("\nHere's the solution!")
                    self.display_matrix()
                    return
                else:
                    print('No solution exists!')
                    return

        # prompts for next move and runs the remainder of game loop
        while user_response := self.get_user_input(self.prompt['nex_msg'], self.error['nex_err'], input_type='nex'):
            if user_response[0] != 'Invalid':
                self.reset_and_move_position(*user_response)
                possible_moves = self.get_possible_movement(user_response)
                self.display_matrix(possible_moves)
                if self.is_all_square_visited():
                    print('\nWhat a great tour! Congratulations!')
                    break
                if self.is_move_possible(user_response):
                    break


if __name__ == '__main__':
    KnightPuzzle().main_processing()
