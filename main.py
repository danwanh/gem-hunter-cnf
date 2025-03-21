# import sys
# from solver import *

# def main():
#     # Khởi tạo Grid
#     grid = Grid("testcases/input_2.txt")
#     cnf = grid.generateCNF()
#     # grid.write_output_board("testcases/output_1.txt")
#     # print(cnf)
#     print("Brute force: ")
#     solver = Solver(grid)

#     ans, time = solver.brute_force()
#     print(ans, time)

#     print("Backtracking: ")
#     ans, time = solver.backtracking()
#     print(ans, time)

#     print("pysat: ")
#     ans, time = solver.use_pysat()
#     print(ans, time)

#     solver.apply_solution(ans)
#     grid.write_output_board("testcases/output_2.txt")


# main()
import sys
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
    grid = Grid(input_file)
    solver = Solver(grid)
    results = []
    
    if algorithm == "bruteforce" or algorithm == "all":
        if(test_case == "11x11" or test_case == "20x20"):
            results.append(["Brute Force", "N/A"])
        else: 
            ans, time = solver.brute_force()
            results.append(["Brute Force", time])
    
    if algorithm == "backtracking" or algorithm == "all":
        ans, time = solver.backtracking()
        results.append(["Backtracking", time])
    
    if algorithm == "pysat" or algorithm == "all":
        ans, time = solver.use_pysat()
        results.append(["PySAT", time])
    
    if results:
        print(tabulate(results, headers=["Algorithm", "Time (s)"], tablefmt="grid"))
    
    solver.apply_solution(ans)
    grid.write_output_board(output_file)
    print(f"Solution written to {output_file}")

if __name__ == "__main__":
    main()
