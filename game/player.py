class Player:
    def __init__(self, x: int, y: int, current_grid):
        self.x = x
        self.y = y
        self.current_grid = current_grid

    def reset_position(self):
        set_x = 2
        set_y = 2
        while self.current_grid.is_box_raw(set_x, set_y):
            set_x += 1
            if set_x >= self.current_grid.get_width() - 1:
                set_y += 1
                set_x = 1
            if set_y >= self.current_grid.get_height() - 1:
                break
        self.x = set_x
        self.y = set_y

    def move_up(self) -> bool:
        new_y = self.y - 1
        if not self.current_grid.is_wall(self.x, new_y):
            if self.current_grid.is_box(self.x, new_y):
                box = self.current_grid.get_box(self.x, new_y)
                if box and box.move_up():
                    self.y = new_y
                    return True
                return False
            else:
                self.y = new_y
                return True
        return False

    def move_down(self) -> bool:
        new_y = self.y + 1
        if not self.current_grid.is_wall(self.x, new_y):
            if self.current_grid.is_box(self.x, new_y):
                box = self.current_grid.get_box(self.x, new_y)
                if box and box.move_down():
                    self.y = new_y
                    return True
                return False
            else:
                self.y = new_y
                return True
        return False

    def move_left(self) -> bool:
        new_x = self.x - 1
        if not self.current_grid.is_wall(new_x, self.y):
            if self.current_grid.is_box(new_x, self.y):
                box = self.current_grid.get_box(new_x, self.y)
                if box and box.move_left():
                    self.x = new_x
                    return True
                return False
            else:
                self.x = new_x
                return True
        return False

    def move_right(self) -> bool:
        new_x = self.x + 1
        if not self.current_grid.is_wall(new_x, self.y):
            if self.current_grid.is_box(new_x, self.y):
                box = self.current_grid.get_box(new_x, self.y)
                if box and box.move_right():
                    self.x = new_x
                    return True
                return False
            else:
                self.x = new_x
                return True
        return False
