"""Implemention of the Maze ADT using a 2-D array."""
from arrays import Array2D
from lliststack import Stack

class Maze:
    """Define constants to represent contents of the maze cells."""
    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    def __init__(self, num_rows, num_cols):
        """Creates a maze object with all cells marked as open."""
        self._maze_cells = Array2D(num_rows, num_cols)
        self._start_cell = None
        self._exit_cell = None

    def num_rows(self):
        """Returns the number of rows in the maze."""
        return self._maze_cells.num_rows()

    def num_cols(self):
        """Returns the number of columns in the maze."""
        return self._maze_cells.num_cols()

    def set_wall(self, row, col):
        """Fills the indicated cell with a "wall" marker."""
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._maze_cells[row, col] = self.MAZE_WALL

    def set_start(self, row, col):
        """Sets the starting cell position."""
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._start_cell = _CellPosition(row, col)

    def set_exit(self, row, col):
        """Sets the exit cell position."""
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._exit_cell = _CellPosition(row, col)


    def find_path(self):
        """
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.
        operation priority: вверх, вправо, вниз, вліво
        """
        solution = Stack()
        solution.push(self._start_cell)
        while True:
            try:
                currow = solution.peek().row
                curcol = solution.peek().col
            except AssertionError:
                # self._maze_cells[self._start_cell.row, self._start_cell.col]=self.PATH_TOKEN
                return False
            if self._exit_found(currow, curcol):
                self._maze_cells[currow, curcol] = self.PATH_TOKEN
                return True
            elif self._valid_move(currow-1, curcol):
                solution.push(_CellPosition(currow-1, curcol))
                self._maze_cells[currow, curcol] = self.PATH_TOKEN
            elif self._valid_move(currow, curcol+1):
                solution.push(_CellPosition(currow, curcol+1))
                self._maze_cells[currow, curcol] = self.PATH_TOKEN
            elif self._valid_move(currow+1, curcol):
                solution.push(_CellPosition(currow+1, curcol))
                self._maze_cells[currow, curcol] = self.PATH_TOKEN
            elif self._valid_move(currow, curcol-1):
                solution.push(_CellPosition(currow, curcol-1))
                self._maze_cells[currow, curcol] = self.PATH_TOKEN
            else:
                self._maze_cells[currow, curcol] = self.TRIED_TOKEN
                try:
                    solution.pop()
                except AssertionError:
                    return False

    def reset(self):
        """Resets the maze by removing all "path" and "tried" tokens."""
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                if self._maze_cells[row, col]==self.PATH_TOKEN or\
                    self._maze_cells[row, col]==self.TRIED_TOKEN:
                    self._maze_cells[row, col] = None

    def __str__(self):
        """Returns a text-based representation of the maze."""
        res=''
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                if self._maze_cells[row, col] is not None:
                    res+=self._maze_cells[row, col]+' '
                else:
                    res+='_ '
            res+='\n'
        return res.strip('\n')

    def _valid_move(self, row, col):
        """Returns True if the given cell position is a valid move."""
        return row >= 0 and row < self.num_rows() \
               and col >= 0 and col < self.num_cols() \
               and self._maze_cells[row, col] is None

    def _exit_found(self, row, col):
        """Helper method to determine if the exit was found."""
        return row == self._exit_cell.row and col == self._exit_cell.col

    def _mark_tried(self, row, col):
        """Drops a "tried" token at the given cell."""
        self._maze_cells[row, col] = self.TRIED_TOKEN

    def _mark_path(self, row, col):
        """Drops a "path" token at the given cell."""
        self._maze_cells[row, col] = self.PATH_TOKEN


class _CellPosition(object):
    """Private storage class for holding a cell position."""
    def __init__(self, row, col):
        self.row = row
        self.col = col

def build_maze(path):
    """maze from file"""
    with open(path, 'r', encoding='utf-8') as file:
        mzf = file.read().split('\n')
    mze=Maze(int(mzf[0][0]), int(mzf[0][2]))
    mze.set_start(int(mzf[1][0]), int(mzf[1][2]))
    mze.set_exit(int(mzf[2][0]), int(mzf[2][2]))
    mzf = mzf[3:-1]
    for row, rowstr in enumerate(mzf):
        for col, el in enumerate(rowstr):
            if el == '*':
                mze.set_wall(row, col)
    return mze

maze = build_maze('./mazefile.txt')
maze.find_path()
print(maze)
print()
maze.reset()
print(maze)
