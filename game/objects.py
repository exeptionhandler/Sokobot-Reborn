class Tile:
    GROUND = 0
    WALL = 1
    BOX = 2
    DESTINATION = 3
    PLAYER = 4

    def __init__(self, status: int, color: int = 0, player_emote: str = "😎"):
        self.status = status
        self.color = color
        self.player_emote = player_emote

    def set_status(self, status: int, color: int = 0):
        self.status = status
        self.color = color

    def get_status(self) -> int:
        return self.status

    def __str__(self) -> str:
        if self.status == self.GROUND:
            return "⬛"
        elif self.status == self.WALL:
            colors = {
                0: "🟥",
                1: "🟧",
                2: "🟨",
                3: "🟩",
                4: "🟦",
                5: "🟪"
            }
            return colors.get(self.color, "🟥")
        elif self.status == self.BOX:
            return "📦"
        elif self.status == self.DESTINATION:
            return "❌"
        elif self.status == self.PLAYER:
            return self.player_emote
        return "⬛"


class Box:
    def __init__(self, x: int, y: int, current_grid):
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.current_grid = current_grid

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

    def move_up(self) -> bool:
        new_y = self.y - 1
        if not self.current_grid.is_wall(self.x, new_y) and not self.current_grid.is_box(self.x, new_y):
            self.y = new_y
            return True
        return False

    def move_down(self) -> bool:
        new_y = self.y + 1
        if not self.current_grid.is_wall(self.x, new_y) and not self.current_grid.is_box(self.x, new_y):
            self.y = new_y
            return True
        return False

    def move_left(self) -> bool:
        new_x = self.x - 1
        if not self.current_grid.is_wall(new_x, self.y) and not self.current_grid.is_box(new_x, self.y):
            self.x = new_x
            return True
        return False

    def move_right(self) -> bool:
        new_x = self.x + 1
        if not self.current_grid.is_wall(new_x, self.y) and not self.current_grid.is_box(new_x, self.y):
            self.x = new_x
            return True
        return False

    def on_destination(self) -> bool:
        return self.current_grid.is_destination(self.x, self.y)

class Destination:
    def __init__(self, x: int, y: int, current_grid):
        self.x = x
        self.y = y
        self.current_grid = current_grid

    def has_box(self, current_grid) -> bool:
        return current_grid.is_wall(self.x, self.y)
