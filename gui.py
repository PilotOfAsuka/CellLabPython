
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


gui_offset_x, gui_offset_y = 10, 0  # Отступы от края ГУИ
line_text_offset = 30  # Высота строки
count_of_cell = 0  # Счетчик кол-во клеток
count_of_food = 0  # Счетчик кол-во органики
count_of_cycle = 0  # Счетчик кол-во циклов

speed_slider = Slider(cfg.width - cfg.gui_offset + gui_offset_x, gui_offset_y + 15 + line_text_offset *
                      4, 190 - gui_offset_x, 10, 1, 60)


def draw_text(text, var, x, y):
    count_text = main.font.render(text + " " + str(var), True, c.WHITE)
    cfg.screen.blit(count_text, (x, y))


def draw_sun_cord():
    pygame.draw.line(cfg.screen, c.BLACK, (genome.sun_coord[0], 0), (genome.sun_coord[0], cfg.height), width=1)
    pygame.draw.line(cfg.screen, c.BLACK, (0, genome.sun_coord[0]),
                     (cfg.width-cfg.gui_offset, genome.sun_coord[0]), width=1)


def draw_border():
    rect = pygame.Rect(0, 0, cfg.width - cfg.gui_offset, cfg.height)
    pygame.draw.rect(cfg.screen, c.BLACK, rect, width=2)


def draw_gui():
    # Отрисовка текста кол-ва клеток
    draw_text("Cells:", count_of_cell, cfg.width - cfg.gui_offset + gui_offset_x, gui_offset_y)
    # Отрисовка текста кол-ва органики
    draw_text("Organic:", count_of_food, cfg.width - cfg.gui_offset + gui_offset_x, gui_offset_y + line_text_offset)
    # Отрисовка текста кол-ва циклов
    draw_text("Cycle:", count_of_cycle, cfg.width - cfg.gui_offset + gui_offset_x, gui_offset_y + line_text_offset * 2)
    # Отрисовка текста "Скорость"
    draw_text("Speed", "", cfg.width - cfg.gui_offset + gui_offset_x, gui_offset_y + line_text_offset * 3)
    speed_slider.draw(cfg.screen)
    draw_text("Temp.:", genome.temp, cfg.width - cfg.gui_offset + gui_offset_x, gui_offset_y + line_text_offset * 5)
    draw_border()
    draw_sun_cord()
