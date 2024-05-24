from misc.vars import world_grid


def move_cell(self, x, y, new_x, new_y):
    """
    Х, y = Передаем текущие координаты клетки
    new_x, new_y = Передаем новые координаты
    И перемещае клетку
    """
    # Освобождаем текущую позицию
    world_grid[y][x] = None
    # Освобождаем позицию клетки с едой
    world_grid[new_y][new_x] = None
    # Перемещаем бота на новую позицию
    world_grid[new_y][new_x] = self
    self.position = new_x, new_y


def get_colors_bias(self, first_min, first_max, second_min, second_max, third_min, third_max):
    colors = (max(min(self.genome.dna[0] % 255, first_max), first_min),
              max(min(self.genome.dna[0] % 255, second_max), second_min),
              max(min(self.genome.dna[0] % 255, third_max), third_min))
    return colors
