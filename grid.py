import itertools
from pysat.solvers import Glucose3

class Grid:
    def __init__(self, file):
        self.board = self.read_input_board(file)
        self.rows = len(self.board)
        self.cols = len(self.board[0])
        self.var_map = self.build_var_map() 

    def build_var_map(self):
        ''' var_map[(0, 0)] = '_' -> 1, var_map[(0, 1)] = 6 -> ignore, var_map[(0, 2)] = '_' -> 2, ... '''
        temp_map = {}
        count = 1
        for r in range(self.rows):
            for c in range(self.cols):
                if(self.board[r][c] == '_'):
                    temp_map[(r, c)] = count
                    count += 1
        self.var_map = temp_map

    def get_var(self, r, c):
        ''' from row, column index get 1, 2, ...'''
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

                    '''Tất cả hàng xóm không là bẫy (-neighbor1 ^ -neighbor2 ^ ...)'''
                    if num_traps == 0:
                        for v in vars_list:
                            cnf_set.add((-v,))  
                        continue

                    '''Toàn bộ hàng xóm là bẫy (neighbor1 ^ neighbor2 ^ ...)'''
                    if num_traps == len(neighbors):
                        for v in vars_list:
                            cnf_set.add((v,))
                        continue

                    '''Ràng buộc "tối đa num_traps": <= num_traps:
                        tức là có thể có 0, 1, ... num_traps hàng xóm là bẫy -> tối đa là num_traps
                        -> chọn tổ hợp bất kì trong num_traps + 1 hàng xóm thì có ít nhất 1 vị trí không là bẫy
                        VD. (-1 V -2) ^ (-1 V -3) ^ (-2 V -3)
                        '''
                    for combo in itertools.combinations(vars_list, num_traps + 1):
                        cnf_set.add(tuple(-v for v in combo)) 

                    '''Ràng buộc "tối thiểu num_traps": >= num_traps:
                        tức là num_traps, num_traps + 1, ... hàng xóm là bẫy -> tối thiểu num_traps
                        -> chọn tổ hợp bất kì trong (số hàng xóm - num_traps + 1) thì có ít nhất 1 vị trí là bẫy
                        VD. (1 V 2) ^ (1 V 3) ^ (2 V 3)
                        '''
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

    def count_traps_and_gems(self):
        traps = 0
        gems = 0
        for r in range(len(self.board)):
                for c in range(len(self.board[0])):
                    if self.board[r][c] == 'G':
                        gems += 1
                    if self.board[r][c] == 'T':
                        traps += 1
        return traps, gems
    
    def apply_solution(self, solution):
        self.build_var_map()
        if solution != None:
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] == '_':
                        self.board[i][j] = 'T' if solution[self.get_var(i, j)] else 'G'
        else:
            print("No solution!")