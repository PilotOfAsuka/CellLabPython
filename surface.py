import configs as cfg
import genome
import func
import objects as objs
# Класс Surface определяет мир или же поверхноть для отрисовки
class Surface:
    def __init__(self, surface):
        self.world = surface
        

        pass
        
    # Функция отрисовки обьектов на Surface
    def draw_objs(self):
        for y in range(cfg.GRID_SIZE_H):
            for x in range(cfg.GRID_SIZE_W):
                obj = cfg.world_grid[y][x]
                if isinstance(obj, genome.BotGenome):
                    func.draw_obj(obj)
                if isinstance(obj, objs.Food):
                    func.draw_obj(obj)
                    
    # Функция обновления обьектов в мире                
    def update_surface():
        for y in range(cfg.GRID_SIZE_H):
            for x in range(cfg.GRID_SIZE_W):
                obj = cfg.world_grid[y][x] 
                if isinstance(obj, genome.BotGenome):      
                    obj.execute_genome()