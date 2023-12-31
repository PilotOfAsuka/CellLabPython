import genome
import func
import objects as objs
import gui
import configs as cfg
import pygame
# Инициализация двумерного массива мира
world_grid = [[None for _ in range(cfg.GRID_SIZE_W)] for _ in range(cfg.GRID_SIZE_H)]  # Мир в котором живут клетки


# Класс Surface определяет мир или же поверхность для отрисовки
class Surface:

    # Функция обновления объектов в мире
    @staticmethod
    def update_surface():
        if gui.start_stop_button.click is True:
            gui.count_of_cycle += 1
        gui.count_of_cell = 0
        gui.count_of_food = 0
        for y in range(cfg.GRID_SIZE_H):
            for x in range(cfg.GRID_SIZE_W):
                obj = world_grid[y][x]
                if obj and not obj.iterated:  # Проверяем, не прошел ли объект уже итерацию
                    if isinstance(obj, genome.BotGenome):
                        if gui.start_stop_button.click is True:
                            obj.execute_genome()
                        obj.draw_obj()
                        gui.count_of_cell += 1
                    elif isinstance(obj, objs.Food):
                        if gui.start_stop_button.click is True:
                            obj.count_of_cycle += 1
                            obj.check_death()
                            obj.move()
                        gui.count_of_food += 1
                        func.draw_obj(obj)
                    obj.iterated = True  # Устанавливаем флаг, что объект уже прошел итерацию

    @staticmethod
    def init_cells():
        # Инициализация начальных клеток в мире
        for _ in range(cfg.START_NUM_OF_CELL):
            free_x, free_y = func.random_position(world_grid)
            bot = genome.Cell(x=free_x, y=free_y)
            world_grid[free_y][free_x] = bot
        pass

    @staticmethod
    def check_iterated():
        for y in range(cfg.GRID_SIZE_H):
            for x in range(cfg.GRID_SIZE_W):
                obj = world_grid[y][x]
                if obj:
                    obj.iterated = False


Surface.init_cells()
