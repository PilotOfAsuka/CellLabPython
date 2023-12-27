import configs as cfg
import pygame
import surface
import colors
import main
import gui
import func
import genome


# Класс Арр определяет окно Pygame и его цикл        
class App:
    def __init__(self):
        self.run = True
        self.screen = cfg.screen
        self.surface = surface.Surface()
        self.gui = gui

    # Обработка Эвентов Pygame
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            gui.speed_slider.handle_event(event)

    # Активация и отрисовка графической части окна            
    def draw(self):
        self.screen.fill(colors.BKG_COLOR)  
        self.surface.draw_objs()
        
    # Основной цикл       
    def loop(self):
        while self.run:
            self.event()
            genome.temp, genome.sun_coord = func.weather_simulation(gui.count_of_cycle)
            self.surface.update_surface()
            self.draw()
            self.gui.draw_gui()
            pygame.display.flip() 
            main.clock.tick(gui.speed_slider.val)  # FPS пока так топорно меняем скорость циклов
    
