from pprint import pprint
import time

class Sudoku:
    def __init__(self, matrix):
        self.matrix = matrix

    def copy(self):
        return Sudoku(self.matrix)

    def set(self, i, j, value):
        self.matrix[i][j] = value


def find_next_zero(sudoku: Sudoku):
    for i in range(len(sudoku.matrix)):
        for j in range(len(sudoku.matrix[i])):
            if not sudoku.matrix[i][j]:
                return i, j


def solve(sudoku: Sudoku):
    s = sudoku.copy()
    x = find_next_zero(s)
    if not x:
        pprint(s.matrix)
        raise Exception()

    i = x[0]
    j = x[1]

    for k in range(1, 10):
        s.matrix[i][j] = k
        if check_validity(s, i, j):
            solve(s)
    s.matrix[i][j] = 0


def check_validity(sudoku: Sudoku, i, j):

    if sudoku.matrix[i][j] in sudoku.matrix[i][:j] or sudoku.matrix[i][j] in sudoku.matrix[i][j+1:]:
        return False

    for i_ in range(9):
        if sudoku.matrix[i_][j] == sudoku.matrix[i][j] and not (i_ == i):
            return False

    start_i = i // 3 * 3
    end_i = start_i + 3
    start_j = j // 3 * 3
    end_j = start_j + 3

    for i_ in range(start_i, end_i):
        for j_ in range(start_j, end_j):
            if sudoku.matrix[i_][j_] == sudoku.matrix[i][j] and not (
                i == i_ and j == j_
            ):
                return False

    return True


def get_sudoku(file_name):
    matrix = []
    with open(file_name) as f:
        for line in f.readlines():
            matrix.append(list(map(lambda x: int(x), line.split())))
    return Sudoku(matrix)


if __name__ == "__main__":
    sudoku = get_sudoku("template.txt")
    start = time.time()
    try:
        solve(sudoku)
    except:
        print(time.time() - start)
