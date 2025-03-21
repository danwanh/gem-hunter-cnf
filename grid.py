import itertools
from pysat.solvers import Glucose3

class Grid:
    def __init__(self, file):
        self.board = self.read_input_board(file)
        self.rows = len(self.board)
        self.cols = len(self.board[0])
        self.var_map = self.build_var_map()

    def build_var_map(self):
        temp_map = {}
        count = 1
        for r in range(self.rows):
            for c in range(self.cols):
                temp_map[(r, c)] = count
                count += 1
        self.var_map = temp_map

    def get_var(self, r, c):
        return self.var_map[(r, c)]
    
    def generateCNF(self):
        cnf_set = set()  

        if self.var_map is None:  
            self.build_var_map()

        for r in range(self.rows):
            for c in range(self.cols):
                if isinstance(self.board[r][c], int):  
                    num_traps = self.board[r][c]

                    neighbors = [
                        (nr, nc)
                        for nr, nc in [
                            (r-1, c-1), (r-1, c), (r-1, c+1),
                            (r, c-1),           (r, c+1),
                            (r+1, c-1), (r+1, c), (r+1, c+1)
                        ]
                        if 0 <= nr < self.rows and 0 <= nc < self.cols
                        and self.board[nr][nc] == '_'
                    ]

                    if not neighbors:
                        continue  

                    vars_list = [self.get_var(nr, nc) for nr, nc in neighbors]

                    # Nếu `num_traps == 0`, thì tất cả hàng xóm là `G`
                    if num_traps == 0:
                        for v in vars_list:
                            cnf_set.add((-v,))  
                        continue

                    # Nếu `num_traps == len(neighbors)`, tất cả hàng xóm là `T`
                    if num_traps == len(neighbors):
                        for v in vars_list:
                            cnf_set.add((v,))
                        continue

                    # Ràng buộc "tối đa num_traps" bẫy (ít nhất 1 ô không phải bẫy)
                    for combo in itertools.combinations(vars_list, num_traps + 1):
                        cnf_set.add(tuple(-v for v in combo))

                    # Ràng buộc "tối thiểu num_traps" bẫy (ít nhất 1 ô phải là bẫy)
                    for combo in itertools.combinations(vars_list, len(vars_list) - num_traps + 1):
                        cnf_set.add(tuple(v for v in combo))

        return [list(clause) for clause in cnf_set]

    def read_input_board(self, file_path):
        with open(file_path, 'r') as f:
            self.board = [line.strip().split(', ') for line in f.readlines()]
            for r in range(len(self.board)):
                for c in range(len(self.board[0])):
                    if self.board[r][c] not in ('_', 'T', 'G'):
                        self.board[r][c] = int(self.board[r][c]) 
        return self.board


    def write_output_board(self, file_path):
        with open(file_path, 'w') as f:
            for row in self.board:
                f.write(', '.join(map(str, row)) + '\n')
