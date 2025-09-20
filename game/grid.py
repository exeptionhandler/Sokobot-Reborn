from typing import List
from .objects import Tile, Box, Destination
from .player import Player
from utils.randomizer import Randomizer


class Grid:
    GROUND = 0
    WALL = 1
    BOX = 2
    DESTINATION = 3
    PLAYER = 4
    MAX_BOXES = 8

    def __init__(self, width: int, height: int, box_count: int, player_emote: str = "😎"):
        self.width = width
        self.height = height
        self.box_count = min(box_count, self.MAX_BOXES)
        self.player_emote = player_emote
        self.color = 0
        self.grid: List[List[Tile]] = []
        self.boxes: List[Box] = []
        self.destinations: List[Destination] = []
        self.player = Player(2, 2, self)
        self.create_boxes()
        self.create_destinations()
        self.player.reset_position()
        self.update_grid()

    def create_boxes(self):
        self.color = Randomizer.next_int(6)
        self.boxes = []
        max_x_range = max(self.width - 4, 1)  # evitar rango negativo o cero
        max_y_range = max(self.height - 4, 1)
        for i in range(self.box_count):
            while True:
                x = Randomizer.next_int(max_x_range) + 2
                y = Randomizer.next_int(max_y_range) + 2
                if x == 2 and y == 2:
                    continue
                position_taken = False
                for box in self.boxes:
                    if (x == box.x and y == box.y) or (x-1 == box.x and y == box.y) or (x+1 == box.x and y == box.y):
                        position_taken = True
                        break
                if not position_taken:
                    self.boxes.append(Box(x, y, self))
                    break

    def create_destinations(self):
        self.destinations = []
        max_x_range = max(self.width - 2, 1)  # evitar rango negativo o cero
        max_y_range = max(self.height - 2, 1)
        for i in range(self.box_count):
            while True:
                x = Randomizer.next_int(max_x_range) + 1
                y = Randomizer.next_int(max_y_range) + 1
                position_taken = False
                for dest in self.destinations:
                    if x == dest.x and y == dest.y:
                        position_taken = True
                        break
                if not position_taken and not self.is_box_raw(x, y):
                    self.destinations.append(Destination(x, y, self))
                    break

    def reset(self):
        for box in self.boxes:
            box.reset()
        self.player.reset_position()
        self.update_grid()

    def reset_map(self):
        self.create_boxes()
        self.create_destinations()
        self.player.reset_position()
        self.update_grid()

    def update_grid(self):
        self.grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if x == 0 or x == self.width-1 or y == 0 or y == self.height-1:
                    row.append(Tile(self.WALL, self.color, self.player_emote))
                else:
                    row.append(Tile(self.GROUND, self.player_emote))
            self.grid.append(row)

        for dest in self.destinations:
            self.grid[dest.y][dest.x] = Tile(self.DESTINATION, player_emote=self.player_emote)

        self.grid[self.player.y][self.player.x] = Tile(self.PLAYER, player_emote=self.player_emote)

        for box in self.boxes:
            if box.on_destination():
                self.grid[box.y][box.x] = Tile(self.WALL, self.color, self.player_emote)
            else:
                self.grid[box.y][box.x] = Tile(self.BOX, player_emote=self.player_emote)

    def get_player(self):
        return self.player

    def is_wall(self, x: int, y: int) -> bool:
        if not self.is_valid_position(x, y):
            return True
        return self.grid[y][x].get_status() == self.WALL

    def is_box(self, x: int, y: int) -> bool:
        if not self.is_valid_position(x, y):
            return False
        return self.grid[y][x].get_status() == self.BOX

    def is_box_raw(self, x: int, y: int) -> bool:
        for box in self.boxes:
            if box.x == x and box.y == y:
                return True
        return False

    def is_destination(self, x: int, y: int) -> bool:
        if not self.is_valid_position(x, y):
            return False
        return self.grid[y][x].get_status() == self.DESTINATION

    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_box(self, x: int, y: int):
        for box in self.boxes:
            if box.x == x and box.y == y:
                return box
        return None

    def has_won(self) -> bool:
        for dest in self.destinations:
            if not dest.has_box(self):
                return False
        return True

    def __str__(self) -> str:
        self.update_grid()
        result = ""
        for row in self.grid:
            for tile in row:
                result += str(tile)
            result += "\n"
        print(f"Grid string:\n{result}")  # para debug, elimina luego
        return result.rstrip("\n")


