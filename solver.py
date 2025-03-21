from grid import *
import time
from itertools import product
class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.grid.build_var_map()  # Tạo ánh xạ biến
        self.cnf = self.grid.generateCNF()
        self.variables = self.get_variables()  

    def get_variables(self):
        """Lấy danh sách các ô '_' để xét làm biến"""
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

                if real_var not in assignment: 
                    unassigned = True
                    continue  

                val = assignment[real_var]  

                if (var > 0 and val) or (var < 0 and not val):  
                    satisfied = True  
                    break  
            # Nếu chưa gán không kết luận False mà trả về True để xét nhánh kế
            if not satisfied and not unassigned:  
                # print(f"Vi phạm CNF tại {clause} với assignment {assignment}")
                return False  

        return True 
    def brute_force(self):
        sat_variables = self.variables
        
        for values in product([True, False], repeat=len(sat_variables)):  
            assignment = {var: val for var, val in zip(sat_variables, values)}  
            
            if self.check_cnf(assignment):  
                return assignment  

        return None 
    
    def backtracking(self, index=0, assignment={}):
        if index == len(self.variables):  
            return assignment if self.check_cnf(assignment) else None

        var = self.variables[index]
      
        for value in [True, False]:  
            assignment[var] = value
            if self.check_cnf(assignment):  
                result = self.backtracking(index + 1, assignment)
                if result:
                    return result 

            assignment.pop(var)  

        return None  

    def use_pysat(self):
            """Dùng thư viện PySAT để tìm nghiệm"""
            solver = Glucose3()
            for clause in self.cnf:
                solver.add_clause(clause)

            if solver.solve():
                model = solver.get_model()
                assignment = {abs(var): (var > 0) for var in model if abs(var) in self.variables}
                return assignment
            else:
                return None
