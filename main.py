from pygame_init_graphic.pygame_cycle import pygame_cycle

# Точка входа: весь pygame-цикл живет отдельно, чтобы main.py оставался маленьким.
if __name__ == "__main__":
    pygame_cycle.start_cycle(run=True)
