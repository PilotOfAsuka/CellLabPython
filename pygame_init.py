import pygame as pg
from vars import RES


# Инициализация Pygame
pg.init()
pg.display.set_caption("CellLab")
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()

font = pg.font.SysFont("Verdana", 25)  # Параметры шрифта
