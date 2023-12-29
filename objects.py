import colors as c
import gui
import surface
import configs as cfg
import genome


# Класс еды просто болванка
class Food:
    def __init__(self, food=50, x=0, y=0, color=c.FOOD_COLOR, genome_number=0):
        self.food = food
        self.color = color
        self.position = x, y
        self.count_of_cycle = 0
        self.genome_number = genome_number

    def move(self):

        x, y = self.position
        new_y = y + 1 if -1 < y + 1 < cfg.GRID_SIZE_H else y
        print(f'OBJ:{self}Old:x={x}, y={y}. new:x={x}, y={new_y}')

        if (not isinstance(surface.world_grid[new_y][x], Food) and
                not isinstance(surface.world_grid[new_y][x], genome.BotGenome)):

            # Освобождаем текущую позицию
            surface.world_grid[y][x] = None
            # Перемещаем бота на новую позицию
            surface.world_grid[new_y][x] = self
            self.position = x, new_y
        pass

    def check_death(self):
        if self.count_of_cycle >= 10000:
            x, y = self.position
            surface.world_grid[y][x] = None
