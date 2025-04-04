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
    
    def sort_variables_by_frequency(self):
        '''Sắp xếp self.variables theo tần suất xuất hiện trong self.cnf'''
        from collections import defaultdict

        # Bước 1: Đếm tần suất xuất hiện của mỗi biến trong CNF
        freq = defaultdict(int)
        for clause in self.cnf:
            for literal in clause:
                var = abs(literal)
                freq[var] += 1

        # Bước 2: Sắp xếp self.variables theo tần suất (giảm dần)
        self.variables.sort(key=lambda var: freq[var], reverse=True)

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
    
    def brute_force(self):
        '''Cải thiện tốc độ: Đánh dấu bằng bit, biến nào True thì bật bit 1'''
        start = time.time()
        sat_variables = self.variables
        num_vars = len(sat_variables)
        
        for bitmask in range(1 << num_vars):  
            assignment = {
                sat_variables[i]: (bitmask & (1 << i)) != 0  
                for i in range(num_vars)
            }

            if self.check_cnf(assignment):  
                return assignment, time.time() - start  

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