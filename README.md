# Gem Hunter: SAT-based Trap and Gem Detection
This project implements a Minesweeper-like game called **Gem Hunter**, where each cell in a grid either contains a **trap** or a **gem**. The game uses logical inference to determine the content of each cell using **SAT solving**, **brute-force search**, and **backtracking**.
Each tile with a number represents the number of traps surrounding it. (number from 1 - 8).
## Goal
Given a grid with some clue numbers (representing the number of adjacent traps), the goal is to:
- Determine which cells contain traps (T) and which contain gems (G).
- Represent the problem in **Conjunctive Normal Form (CNF)**.
- Solve it using:
  - A **SAT solver** (using the `pysat` library).
  - A **brute-force algorithm**.
  - A **backtracking algorithm**.
- Compare the performance of each method.
## How to test
Install dependencies:
```sh
pip install -r requirements.txt
```
Execute the program with the desired algorithm and test case by running:
```sh
python main.py <algorithm> <test_case>
```

- Available algorithms: bruteforce, backtracking, pysat, all
- Available test cases: 5x5, 9x9, 11x11, 20x20

## Result
The input grids used for testing are provided in the following files:

- `input_1.txt` → Grid size: **5x5**
- `input_2.txt` → Grid size: **9x9**
- `input_3.txt` → Grid size: **11x11**
- `input_4.txt` → Grid size: **20x20**

After running the program, the corresponding outputs are saved to:

- `output_1.txt` → Result for **5x5** grid
- `output_2.txt` → Result for **9x9** grid
- `output_3.txt` → Result for **11x11** grid
- `output_4.txt` → Result for **20x20** grid
  
Result for my test cases:

| Algorithm     | 5x5        | 9x9        | 11x11     | 20x20      |
|---------------|------------|------------|-----------|------------|
| **Brute force**   | 0.021594   | 12093.1    | > 4 hours | > 4 hours  |
| **Backtracking**  | 0.00140429 | 0.00078392 | 0.001973629 | 0.513217449 |
| **PySAT**         | 0.000170231| 0.000129223| 0.000169039 | 0.000448227 |
