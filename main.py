# ИмПоРтЫ
import pygame
import app

# Инициализация Pygame
pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font("font/REDENSEK.TTF", 35)  # Выберите подходящий шрифт и размер

# Main.py :D
if __name__ == "__main__":
    app = app.App()
    app.loop()
