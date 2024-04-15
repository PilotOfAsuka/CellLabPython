import vars as cfg
import pygame
import simulation
import colors
import main
import gui
import func
import genome
import objects


# Класс Арр определяет окно Pygame и его цикл        
class App:
    def __init__(self):
        self.run = True
        self.screen = cfg.screen
        self.surface = surface.Surface()
        self.gui = gui
        self.obj = objects

    # Обработка Эвентов Pygame
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            gui.start_stop_button.handle_event(event)
            gui.camera.handle_event(event)

    # Активация и отрисовка графической части окна
    def draw(self):
        self.screen.fill(colors.BKG_COLOR)

    # Основной цикл
    def loop(self):
        while self.run:

            self.gui.camera.update()
            self.draw()
            #self.surface.check_iterated()
            genome.temp, genome.sun_coord = func.weather_simulation(gui.count_of_cycle)
            #self.surface.update_surface()
            self.gui.draw_gui()
            self.event()
            pygame.display.flip()
            main.clock.tick(60)  # FPS пока так топорно меняем скорость циклов
    
