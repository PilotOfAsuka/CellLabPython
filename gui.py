
import configs as cfg
import colors as c
import main
import pygame
import genome


# Класс Slider
class Slider:
    def __init__(self, x, y, w, h, min_val, max_val):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val  # Минимальное значение
        self.max_val = max_val  # Максимальное значение
        self.val = min_val  # Значение слайдера
        self.dragging = False  # Нажат или нет

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
                self.val = (max(min((mouse_x - self.rect.x) / self.rect.width, 1), 0) *
                            (self.max_val - self.min_val) + self.min_val)

    # Отрисовка слайдера
    def draw(self, screen):
        pygame.draw.rect(screen, c.WHITE, self.rect)
        slider_pos = int((self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        pygame.draw.rect(screen, c.FOOD_COLOR, (self.rect.x + slider_pos, self.rect.y, 20, self.rect.height))


class Button:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.click = True
        self.stop_color = (0, 155, 0)
        self.start_color = (155, 0, 0)
        self.clicked_text = 'Stop'
        self.non_clicked_text = 'Play'
        self.x = x
        self.y = y

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.click is True:
                self.click = False
            else:
                self.click = True

    def draw(self, screen):
        if self.click is True:
            pygame.draw.rect(screen, self.start_color, self.rect)
            count_text = main.font.render(self.clicked_text, True, c.WHITE)
            cfg.screen.blit(count_text, (self.x, self.y - 5))
        else:
            pygame.draw.rect(screen, self.stop_color, self.rect)
            count_text = main.font.render(self.non_clicked_text, True, c.WHITE)
            cfg.screen.blit(count_text, (self.x, self.y - 6))


gui_offset_x, gui_offset_y = 10, 0  # Отступы от края ГУИ
line_text_offset = 30  # Высота строки
count_of_cell = 0  # Счетчик кол-во клеток
count_of_food = 0  # Счетчик кол-во органики
count_of_cycle = 0  # Счетчик кол-во циклов

camera = cfg.Camera(cfg.width-200, cfg.height)

start_stop_button = Button(cfg.width - cfg.gui_offset + gui_offset_x, gui_offset_y + 7 + line_text_offset *
                      3, 80, 25)


def draw_text(text, var, x, y):
    count_text = main.font.render(text + " " + str(var), True, c.WHITE)
    cfg.screen.blit(count_text, (x, y))

def draw_gui_rect(screen):
    rect = pygame.Rect(cfg.width - 200, 0, 200, cfg.height)
    pygame.draw.rect(screen, (117, 104, 84), rect)


def draw_border():
    rect = pygame.Rect(0, 0, cfg.width - cfg.gui_offset, cfg.height)
    pygame.draw.rect(cfg.screen, c.BLACK, rect, width=2)


def draw_gui():
    draw_gui_rect(cfg.screen)
    # Отрисовка текста кол-ва клеток
    draw_text("Cells:", count_of_cell, cfg.width - cfg.gui_offset + gui_offset_x, gui_offset_y)
    # Отрисовка текста кол-ва органики
    draw_text("Organic:", count_of_food, cfg.width - cfg.gui_offset + gui_offset_x, gui_offset_y + line_text_offset)
    # Отрисовка текста кол-ва циклов
    draw_text("Cycle:", count_of_cycle, cfg.width - cfg.gui_offset + gui_offset_x, gui_offset_y + line_text_offset * 2)
    # Отрисовка текста "Скорость"
    draw_text("Temp.:", genome.temp, cfg.width - cfg.gui_offset + gui_offset_x, gui_offset_y + line_text_offset * 4)
    draw_border()
    start_stop_button.draw(cfg.screen)
