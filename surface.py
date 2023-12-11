import configs as cfg
import genome
import func
import objects as objs
import gui

# Инициализация двумерного массива мира
world_grid = [[None for _ in range(cfg.GRID_SIZE_W)] for _ in range(cfg.GRID_SIZE_H)] # Мир в котором живут клетки

# Инициализация начальных клеток в мире
for _ in range(cfg.START_NUM_OF_CELL):
    x, y = func.random_position(world_grid)
    bot = genome.Cell(x=x, y=y)
    world_grid[y][x] = bot
for _ in range(cfg.START_NUM_OF_CELL):
    x, y = func.random_position(world_grid)
    bot = genome.Predator(x=x, y=y)
    world_grid[y][x] = bot
    
# Класс Surface определяет мир или же поверхноть для отрисовки
class Surface:
    def __init__(self, surface):
        self.world = surface
        pass
        
    # Функция отрисовки обьектов на Surface
    def draw_objs(self):
        gui.count_of_cell = 0
        gui.count_of_food = 0
        func.count_of_cell = 0
        func.count_of_food = 0
        for y in range(cfg.GRID_SIZE_H):
            for x in range(cfg.GRID_SIZE_W):
                obj = world_grid[y][x]
                if isinstance(obj, genome.BotGenome):
                    func.draw_obj(obj)
                    gui.count_of_cell += 1
                    func.count_of_cell += 1
                if isinstance(obj, objs.Food):
                    gui.count_of_food += 1
                    func.count_of_food += 1
                    func.draw_obj(obj)
                    
    # Функция обновления обьектов в мире                
    def update_surface():
        for y in range(cfg.GRID_SIZE_H):
            for x in range(cfg.GRID_SIZE_W):
                obj = world_grid[y][x] 
                if isinstance(obj, genome.BotGenome):      
                    obj.execute_genome()