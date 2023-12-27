import configs as cfg
import genome
import func
import objects as objs
import gui

# Инициализация двумерного массива мира
world_grid = [[None for _ in range(cfg.GRID_SIZE_W)] for _ in range(cfg.GRID_SIZE_H)]  # Мир в котором живут клетки


# Класс Surface определяет мир или же поверхность для отрисовки
class Surface:
    # Функция отрисовки объектов на Surface
    @staticmethod
    def draw_objs():
        gui.count_of_cell = 0
        gui.count_of_food = 0
        gui.count_of_cycle += 1
        for y in range(cfg.GRID_SIZE_H):
            for x in range(cfg.GRID_SIZE_W):
                obj = world_grid[y][x]
                if isinstance(obj, genome.BotGenome):
                    func.draw_obj(obj)
                    gui.count_of_cell += 1
                if isinstance(obj, objs.Food):
                    gui.count_of_food += 1
                    func.draw_obj(obj)

    # Функция обновления объектов в мире
    @staticmethod
    def update_surface():
        for y in range(cfg.GRID_SIZE_H):
            for x in range(cfg.GRID_SIZE_W):
                obj = world_grid[y][x]
                if isinstance(obj, genome.BotGenome):
                    obj.execute_genome()

    @staticmethod
    def init_cells():
        # Инициализация начальных клеток в мире
        for _ in range(cfg.START_NUM_OF_CELL):
            free_x, free_y = func.random_position(world_grid)
            bot = genome.Cell(x=free_x, y=free_y)
            world_grid[free_y][free_x] = bot
        pass


Surface.init_cells()
