from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
        print("window closed")

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color='black'):
        line.draw(self.canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2

    def draw(self, canvas, fill_color='black'):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)


class Cell:
    def __init__(self, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._window = window
        self.visited = False
    
    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        corner1 = Point(x1, y1)
        corner2 = Point(x1, y2)
        corner3 = Point(x2, y1)
        corner4 = Point(x2, y2)

        if self.has_left_wall:
            self._window.draw_line(Line(corner1, corner2))
        else:
            self._window.draw_line(Line(corner1, corner2), 'white')
        if self.has_right_wall:
            self._window.draw_line(Line(corner3, corner4))   
        else:
            self._window.draw_line(Line(corner3, corner4), 'white')        
        if self.has_top_wall:
            self._window.draw_line(Line(corner1, corner3))
        else:
            self._window.draw_line(Line(corner1, corner3), 'white')
        if self.has_bottom_wall:
            self._window.draw_line(Line(corner2, corner4))
        else:
            self._window.draw_line(Line(corner2, corner4), 'white')

    def draw_move(self, to_cell, undo=False):
        center_from = Point((self._x1+self._x2)/2, (self._y1+self._y2)/2)
        center_to = Point((to_cell._x1+to_cell._x2)/2, (to_cell._y1+to_cell._y2)/2)
        line = Line(center_from, center_to)

        if undo:
            self._window.draw_line(line, fill_color='gray')
        else:
            self._window.draw_line(line, fill_color='red')
