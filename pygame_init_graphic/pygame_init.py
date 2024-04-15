import pygame as pg
from misc.vars import RES


# Инициализация Pygame
pg.init()
pg.display.set_caption("CellLab")
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()


font = pg.font.Font("font/REDENSEK.TTF", 35)  # Параметры шрифта
