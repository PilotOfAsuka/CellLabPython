import colors as c


# Класс еды просто болванка
class Food:
    def __init__(self, world, food=0, x=0, y=0, color=c.FOOD_COLOR):
        self.world = world
        self.food = food
        self.color = color
        self.position = x, y        
        