# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: *The naked twins technique enforces a new constraint in the unit containing both boxes. No boxes in the unit can contain the values of the naked twins. The technique is described as follows: At first, one need to find if there are any two boxes belonging to the same unit with equal two (and only two) possible values. If yes, these boxes are the naked twins and one must remove these two possible values from all peers in unit, except from the naked twins themselves. The resulting sudoku can now be further reduced with the elimination and only choice techiques.*

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: *The diagonal sudoku problem enforces a new constraint in the main and secondary diagonals of the sudoku grid. The boxes in each of these diagonals form a new unit. The constraint propagation techniques, such as the elimination, only choice and naked twins, must include these new units in order to solve the diagonal sudoku.*

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.