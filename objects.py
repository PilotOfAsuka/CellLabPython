import colors as c
import gui
import simulation
import vars as cfg
import genome
import pygame


# Класс еды просто болванка
class Food:
    def __init__(self, food=50, x=0, y=0, color=c.FOOD_COLOR, genome_number=0):
        self.food = food
        self.color = color
        self.position = x, y
        self.count_of_cycle = 0
        self.genome_number = genome_number
        self.iterated = False
        self.click = False

    def move(self):
        """
        Перемещение объекта
        """
        x, y = self.position
        new_y = y + 1 if -1 < y + 1 < cfg.GRID_SIZE_H else y

        if (not isinstance(surface.world_grid[new_y][x], Food) and
                not isinstance(surface.world_grid[new_y][x], genome.BotGenome)):
            if gui.count_of_cycle % 1 == 0:
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

    def draw_obj(self, border_size=1):
        """
        Отрисовка объекта
        """
        x, y = self.position
        rect = pygame.Rect((x + gui.camera.x_offset) * (cfg.CELL_SIZE * gui.camera.scale),
                           (y + gui.camera.y_offset) * (cfg.CELL_SIZE * gui.camera.scale),
                           (cfg.CELL_SIZE * gui.camera.scale), (cfg.CELL_SIZE * gui.camera.scale))
        pygame.draw.rect(cfg.screen, self.color, rect)
        self.rect = rect
        border_rect = rect.inflate(border_size * 2, border_size * 2)
        if self.click is True:  # Обводка
            pygame.draw.rect(cfg.screen, c.BLACK, border_rect, border_size)