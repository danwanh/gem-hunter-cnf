import sys
import copy
from solver import *
from tabulate import tabulate

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <algorithm> <test_case>")
        print("Available algorithms: bruteforce, backtracking, pysat, all")
        print("Available test cases: 5x5, 11x11, 20x20, 9x9")
        return
    
    algorithm = sys.argv[1].lower()
    test_case = sys.argv[2].lower()
    
    test_cases = {
        "5x5": ("testcases/input_1.txt", "testcases/output_1.txt"),
        "11x11": ("testcases/input_2.txt", "testcases/output_2.txt"),
        "20x20": ("testcases/input_3.txt", "testcases/output_3.txt"),
        "9x9": ("testcases/input_4.txt", "testcases/output_4.txt"),
    }
    
    if test_case not in test_cases:
        print("Invalid test case. Choose from: 5x5, 11x11, 20x20, 9x9")
        return
    
    input_file, output_file = test_cases[test_case]
    
    # Tạo grid gốc
    original_grid = Grid(input_file)
    
    
    results = []
    final_solution = None
    
    if algorithm in {"bruteforce", "all"}:
        grid = copy.deepcopy(original_grid)
        solver = Solver(grid)
        if test_case in {"11x11", "20x20"}:
            print("Number of variable assignments for brute force is", len(solver.variables)) 
            print("In brute force, there are 2 ^", len(solver.variables), "possible assignments, which results in a very long execution time (> 3 hours).")
            results.append(["Brute Force", " ", " ", "> 3 hours"])
        else:
            ans, time = solver.brute_force()
            grid.apply_solution(ans)
            traps, gems = grid.count_traps_and_gems()
            results.append(["Brute Force", traps, gems, time])
            final_solution = ans  
    
    if algorithm in {"backtracking", "all"}:
        grid = copy.deepcopy(original_grid)
        solver = Solver(grid)
        ans, time = solver.backtracking()
        grid.apply_solution(ans)
        traps, gems = grid.count_traps_and_gems()
        results.append(["Backtracking", traps, gems, time])
        final_solution = ans
    
    if algorithm in {"pysat", "all"}:
        grid = copy.deepcopy(original_grid)
        solver = Solver(grid)
        ans, time = solver.use_pysat()
        grid.apply_solution(ans)
        traps, gems = grid.count_traps_and_gems()
        results.append(["PySAT", traps, gems, time])
        final_solution = ans
    
    if results:
        print(tabulate(results, headers=["Algorithm", "Traps", "Gems", "Time (s)"], tablefmt="fancy_grid"))
    print("Number of CNF clauses: ", len(solver.cnf))
    if final_solution:
        original_grid.apply_solution(final_solution)
        original_grid.write_output_board(output_file)
        print(f"Solution written to {output_file}")
    # print(solver.cnf)

if __name__ == "__main__":
    main()