# ИмПоРтЫ
import pygame
import app

# Инициализация Pygame
pygame.init()
clock = pygame.time.Clock()

# Main.py :D  
if __name__ == "__main__":
    app = app.App()
    app.loop()