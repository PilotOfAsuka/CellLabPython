
from misc.vars import world_grid, GRID_SIZE_H
from misc import colors as c


class Food:
    def __init__(self, food=50, x=0, y=0, color=c.FOOD_COLOR, genome_number=0):
        self.food = food
        self.color = color
        self.position = x, y
        self.x, self.y = self.position
        self.count_of_cycle = 0
        self.count_of_life = 0
        self.genome_number = genome_number

    def move(self):
        """
        Перемещение объекта
        """
        x, y = self.position
        new_y = y + 1 if -1 < y + 1 < GRID_SIZE_H else y

        if world_grid[new_y][x].__class__.__name__ not in ("Food", "BotGenome"):
            # Освобождаем текущую позицию
            world_grid[y][x] = None
            # Перемещаем бота на новую позицию
            world_grid[new_y][x] = self
            self.position = x, new_y
        pass

    def check_death(self):
        if self.count_of_life >= 50000:
            x, y = self.position
            world_grid[y][x] = None

    def draw_obj(self):
        """
        Отрисовка объекта
        """

