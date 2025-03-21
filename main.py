import sys
from solver import *

def main():
    # board = [
    #     [1, '_'],
    #     ['_', 1]
    # ]

    board = [
    [3, '_', 2, '_'],
    ['_', '_', 2, '_'],
    ['_', 3, 1, '_']
    ]
    # Khởi tạo Grid
    grid = Grid(board)
    cnf = grid.generateCNF()
    grid.write_output_board("put.txt")
    print(cnf)
    print("-------------------------------------")
    solver = Solver(grid)

    print(solver.brute_force())
    print(solver.backtracking())
    print("---------------------------------------")
    print(solver.use_pysat())

main()
