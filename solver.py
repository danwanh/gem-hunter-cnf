from grid import *
import time
from itertools import product
from collections import Counter

class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.grid.build_var_map() 
        self.cnf = self.grid.generateCNF()
        self.variables = self.get_variables() # Các biến SAT có giá trị _

    def get_variables(self):
        '''Lấy các SAT variables có mà trong board có giá trị _'''
        variables = []
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                if self.grid.board[r][c] == "_":  
                    variables.append(self.grid.get_var(r, c))  
        return variables

    def check_cnf(self, assignment):
        for clause in self.cnf:
            satisfied = False  
            unassigned = False  

            for var in clause:
                real_var = abs(var)
                '''Ignore unasigned variables (when backtracking), only conclude False when all var is assigned 
                    else conclude True'''
                if real_var not in assignment: 
                    unassigned = True
                    continue  

                val = assignment[real_var]  
                '''P = True or -P = False -> clause = True'''
                if (var > 0 and val) or (var < 0 and not val):  
                    satisfied = True  
                    break  
            '''If clause is False and all variables in clause assigned -> CNF False'''
            if not satisfied and not unassigned:  
                return False  
        '''All clause is True -> CNF True'''
        return True 
    
    # def brute_force(self):
    #     '''Dùng bitmask'''
    #     start = time.time()

    #     sat_variables = self.variables
    #     check_cnf = self.check_cnf  # Tránh truy cập self nhiều lần

    #     num_vars = len(sat_variables)
    #     max_state = 1 << num_vars  

    #     for bitmask in range(max_state):
    #         # Duyệt tổ hợp bằng bitmask
    #         assignment = {}
    #         for i in range(num_vars):
    #             assignment[sat_variables[i]] = (bitmask >> i) & 1 == 1

    #         if check_cnf(assignment):
    #             return assignment, time.time() - start

    #     return None, time.time() - start
    
    def brute_force(self):
        '''Brute-force nhanh hơn với list + bitmask + tần suất biến'''
        import time
        start = time.time()

        var_list = self.variables
        num_vars = len(var_list)

        # Tạo ánh xạ: var_id -> index trong bitmask
        var_to_index = {var: idx for idx, var in enumerate(var_list)}

        assignment = [False] * num_vars

        # Sắp xếp clause theo độ dài và tần suất biến để detect sai sớm hơn
        var_freq = Counter()
        for clause in self.cnf:
            for v in clause:
                if abs(v) in var_to_index:
                    var_freq[abs(v)] += 1
        self.cnf.sort(key=lambda c: sum(var_freq[abs(v)] for v in c))

        max_state = 1 << num_vars
        for bitmask in range(max_state):
            for i in range(num_vars):
                assignment[i] = (bitmask >> i) & 1 == 1

            # Kiểm tra CNF
            satisfied_all = True
            for clause in self.cnf:
                satisfied_clause = False
                for var in clause:
                    if abs(var) not in var_to_index:
                        continue  # ignore biến không cần xét

                    idx = var_to_index[abs(var)]
                    val = assignment[idx]
                    if (var > 0 and val) or (var < 0 and not val):
                        satisfied_clause = True
                        break
                if not satisfied_clause:
                    satisfied_all = False
                    break

            if satisfied_all:
                result = {var_list[i]: assignment[i] for i in range(num_vars)}
                return result, time.time() - start

        return None, time.time() - start

    def backtracking(self, index = 0, assignment = None, start_time = None):
        if start_time is None:
            start_time = time.time()
        
        if assignment is None:
            assignment = {}

        if index == len(self.variables):  
            return (assignment if self.check_cnf(assignment) else None), time.time() - start_time

        var = self.variables[index]

        ordered_values = [False, True]  # Order: False → True
        
        for value in ordered_values:  
            assignment[var] = value
            if self.check_cnf(assignment):  
                result, elapsed_time = self.backtracking(index + 1, assignment, start_time)
                if result:
                    return result, elapsed_time  
            
            assignment.pop(var)  

        return None, time.time() - start_time

    def use_pysat(self):
            start = time.time()
            solver = Glucose3()
            for clause in self.cnf:
                solver.add_clause(clause)
                
            if solver.solve():
                model = solver.get_model()
                assignment = {abs(var): (var > 0) for var in model if abs(var) in self.variables}
                end = time.time()
                return assignment, end - start
            else:
                end = time.time()
                return None, end - start
            
    

    