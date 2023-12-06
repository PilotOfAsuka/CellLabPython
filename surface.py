import configs as cfg
import genome
import func
import objects as objs
# Класс Surface определяет мир или же поверхноть для отрисовки
class Surface:
    def __init__(self, screen):
        self.screen = screen
    # Функция отрисовки ВСЕХ обьектов на Surface
    def draw_objs(self):
        for y in range(cfg.GRID_SIZE_H):
            for x in range(cfg.GRID_SIZE_W):
                obj = cfg.world_grid[y][x]
                if isinstance(obj, genome.BotGenome):
                    obj.execute_genome()
                    func.draw_bot(obj)
                if isinstance(obj, objs.Food):
                    func.draw_bot(obj)