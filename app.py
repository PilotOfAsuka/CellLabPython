import configs as cfg
import pygame
import surface
import colors
import main
# Класс Арр определяет окно Pygame и его цикл        
class App:
    def __init__(self):
        self.run = True
        self.screen = cfg.screen
        self.surface = surface.Surface(self.screen)
        
    # Обработка Евентов Pygame    
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    # Активация и отрисовка графической части окна            
    def draw(self):
        self.screen.fill(colors.BKG_color)  
        self.surface.draw_objs()
        
    # Основной цикл       
    def loop(self):
        while self.run:
            self.draw()
            self.event()
            pygame.display.flip() # из за этой стройки мучался блин , черный экран был
            main.clock.tick(cfg.FPS)# ФПС ННАДА!!