import random

from misc import vars

grid_h = 3
grid_w = 3
size = grid_w * grid_h

def get_coord_from_index(index):
    y = index // grid_w
    x = index % grid_w

    return x, y

def get_index(x, y):
    return y * grid_w + x


class Cell_2d:
    def __init__(self, position, index):
        self.x, self.y = position

    def reproduce(self):
        free_positions = get_free_adjacent_positions((self.x, self.y))

        if not free_positions:
            return

        new_x, new_y = free_positions[random.randint(0, len(free_positions)) - 1]

        new_index = get_index(new_x, new_y)

        new_cell = Cell_2d(position=(new_x, new_y), index=new_index)

        world_grid_2d[new_index] = new_cell



world_grid_2d = [None for _ in range(size)]

def init_cels(nums):
    for num in range(nums):
        world_grid_2d[num] = Cell_2d(position=get_coord_from_index(num), index=num)





def get_free_adjacent_positions(position):
    x, y = position
    free_positions = []
    for dx, dy in vars.move_directions:
        nx = x + dx if -1 < x + dx < grid_w else x
        ny = y + dy if -1 < y + dy < grid_h else y
        if world_grid_2d[get_index(nx, ny)] is None:
            free_positions.append((nx, ny))
    return free_positions  # Возврат свободных позиций


init_cels(2)

print(world_grid_2d)

for obj in world_grid_2d:
    if obj is not None:
        obj.reproduce()

print(world_grid_2d)