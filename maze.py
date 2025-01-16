from cells import Cell
import time
import random

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        window=None,
        seed=None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._window = window
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)

    def _create_cells(self):     
        for i in range(self.num_cols):
            column = []
            for j in range(self.num_rows):
                column.append(Cell(self._window))
            self._cells.append(column)
                

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
    
    def _draw_cell(self, i, j):
        if self._window is None:
            return
        self._cells[i][j].draw(self._x1+i*self.cell_size_x, self._y1+j*self.cell_size_y, self._x1+(i+1)*self.cell_size_x, self._y1+(j+1)*self.cell_size_y)
        self._animate()

    def _animate(self):
        if self._window is None:
            return
        self._window.redraw()
        time.sleep(0.02)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = False
        self._draw_cell(self.num_cols-1, self.num_rows-1)
    
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            
            if i > 0 and not self._cells[i-1][j].visited:
                to_visit.append((i-1, j))
            if i < self.num_cols - 1 and not self._cells[i+1][j].visited:
                to_visit.append((i+1, j))
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit.append((i,j-1))
            if j < self.num_rows - 1 and not self._cells[i][j+1].visited:
                to_visit.append((i,j+1))
            
            if not to_visit:
                self._draw_cell(i,j)
                return
            
            random_index = random.randrange(len(to_visit))
            next_cell = to_visit[random_index]

            if next_cell[0] == i-1:
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False

            if next_cell[0] == i+1:
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False

            if next_cell[1] == j-1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False

            if next_cell[1] == j+1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False
            
            self._break_walls_r(next_cell[0], next_cell[1])

    
