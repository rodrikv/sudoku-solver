from pprint import pprint
import time


class Sudoku:
    def __init__(self, matrix):
        self.matrix = matrix
        self.size = 9
        self.block_size = 3
        self.rows = [set(range(1, 10)) for _ in range(self.size)]
        self.cols = [set(range(1, 10)) for _ in range(self.size)]
        self.blocks = [set(range(1, 10)) for _ in range(self.size)]
        self._initialize_sets()

    def _initialize_sets(self):
        for i in range(self.size):
            for j in range(self.size):
                value = self.matrix[i][j]
                if value:
                    if value in self.rows[i] and value in self.cols[j] and value in self.blocks[self._block_index(i, j)]:
                        self.rows[i].discard(value)
                        self.cols[j].discard(value)
                        self.blocks[self._block_index(i, j)].discard(value)
                    else:
                        raise ValueError(f"Invalid Sudoku: Duplicate value {value} at position ({i}, {j})")

    def _block_index(self, i, j):
        return (i // self.block_size) * self.block_size + (j // self.block_size)

    def set_value(self, i, j, value):
        self.matrix[i][j] = value
        self.rows[i].discard(value)
        self.cols[j].discard(value)
        self.blocks[self._block_index(i, j)].discard(value)

    def unset_value(self, i, j, value):
        self.matrix[i][j] = 0
        self.rows[i].add(value)
        self.cols[j].add(value)
        self.blocks[self._block_index(i, j)].add(value)

    def get_candidates(self, i, j):
        return (
            self.rows[i]
            & self.cols[j]
            & self.blocks[self._block_index(i, j)]
        )


def find_next_zero(sudoku: Sudoku):
    for i in range(sudoku.size):
        for j in range(sudoku.size):
            if sudoku.matrix[i][j] == 0:
                return i, j
    return None


def solve(sudoku: Sudoku):
    next_pos = find_next_zero(sudoku)
    if not next_pos:
        pprint(sudoku.matrix)
        return True

    i, j = next_pos
    for candidate in sudoku.get_candidates(i, j):
        sudoku.set_value(i, j, candidate)
        if solve(sudoku):
            return True
        sudoku.unset_value(i, j, candidate)

    return False


def get_sudoku(file_name):
    matrix = []
    with open(file_name) as f:
        for line in f:
            matrix.append(list(map(int, line.split())))
    return Sudoku(matrix)


if __name__ == "__main__":
    try:
        sudoku = get_sudoku("template.txt")
        start = time.time()
        if not solve(sudoku):
            print("No solution exists.")
        print(f"Time taken: {time.time() - start:.4f} seconds")
    except ValueError as e:
        print(e)
