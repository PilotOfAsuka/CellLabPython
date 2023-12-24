
import configs as cfg
import colors as c
import main
import pygame
import genome
# Класс Slider
class Slider:
    def __init__(self, x, y, w, h, min_val, max_val):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val # Минимальное значение
        self.max_val = max_val # Максимальное значение
        self.val = min_val # Значение слайдера
        self.dragging = False # Нажат или нет
    # Обработка событий слайдера
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, _ = event.pos
                self.val = max(min((mouse_x - self.rect.x) / self.rect.width, 1), 0) * (self.max_val - self.min_val) + self.min_val
    # Отрисовка слайдера
    def draw(self, screen):
        pygame.draw.rect(screen, c.WHITE, self.rect)
        slider_pos = int((self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        pygame.draw.rect(screen, c.FOOD_COLOR, (self.rect.x + slider_pos, self.rect.y, 20, self.rect.height))
    
gui_ofset_x, gui_ofset_y = 10, 0 # Отступы от края ГУИ  
line_text_ofset = 30 # Высота строки
count_of_cell = 0 # Счетчик кол-во клеток
count_of_food = 0 # Счетчик кол-во органики
count_of_cicle = 0 # Счетчик кол-во циклов

speed_slider = Slider(cfg.width - cfg.gui_ofset + gui_ofset_x, gui_ofset_y + 15 + line_text_ofset * 4, 190 - gui_ofset_x, 10, 1, 60)

def draw_text(text, var,x, y):
    count_text = main.font.render(text +" "+ str(var), True, c.WHITE)
    cfg.screen.blit(count_text, (x,y))

def draw_sun_cord():
    pygame.draw.line(cfg.screen, c.BLACK, (genome.sun_coord[0],0), (genome.sun_coord[0], cfg.height), width=1)
    pygame.draw.line(cfg.screen, c.BLACK, (0,genome.sun_coord[0]), (cfg.width-cfg.gui_ofset, genome.sun_coord[0]), width=1)

def draw_border():
    rect = pygame.Rect(0, 0, cfg.width - cfg.gui_ofset, cfg.height)
    pygame.draw.rect(cfg.screen, c.BLACK, rect, width=2)

def draw_gui():
    # Отрисовка текста кол-ва клеток
    draw_text("Cells:",count_of_cell,cfg.width - cfg.gui_ofset + gui_ofset_x , gui_ofset_y) # (Текст, Переменная(для счета), х,y)
    # Отрисовка текста кол-ва органики
    draw_text("Organic:", count_of_food,cfg.width - cfg.gui_ofset + gui_ofset_x , gui_ofset_y + line_text_ofset)  # Меняйте положение текста при необходимости
    # Отрисовка текста кол-ва циклов
    draw_text("Cycle:", count_of_cicle,cfg.width - cfg.gui_ofset + gui_ofset_x , gui_ofset_y + line_text_ofset * 2)  # Меняйте положение текста при необходимости
    # Отрисовка текста "Скорость"
    draw_text("Speed","",cfg.width - cfg.gui_ofset + gui_ofset_x , gui_ofset_y + line_text_ofset * 3)
    speed_slider.draw(cfg.screen)
    draw_text("Temp.:",genome.temp,cfg.width - cfg.gui_ofset + gui_ofset_x , gui_ofset_y + line_text_ofset * 5)
    draw_border()
    draw_sun_cord()