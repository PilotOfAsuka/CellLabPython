import unittest

from genome import Cell, Food
from misc.func import get_global_var
from misc.vars import GRID_SIZE_H, GRID_SIZE_W, global_vars, world_grid
from simulation import calculate_surface, update_simulation


def reset_world():
    for y in range(GRID_SIZE_H):
        for x in range(GRID_SIZE_W):
            world_grid[y][x] = None
    global_vars.update({"count_of_cycle": 0, "count_of_food": 0, "count_of_cells": 0, "temp": 0})


class SimulationTests(unittest.TestCase):
    def setUp(self):
        reset_world()

    def test_paused_update_does_not_advance_cycle(self):
        update_simulation(is_running=False)

        self.assertEqual(get_global_var("count_of_cycle"), 0)

    def test_food_moves_only_once_per_cycle(self):
        food = Food(x=0, y=0)
        world_grid[0][0] = food

        calculate_surface()

        self.assertIsNone(world_grid[0][0])
        self.assertIs(world_grid[1][0], food)
        self.assertEqual(food.count_of_life, 1)
        self.assertEqual(food.count_of_cycle, 1)
        self.assertEqual(get_global_var("count_of_cycle"), 1)

    def test_newborn_cell_waits_until_next_cycle(self):
        genome = [0] * 64
        genome[1] = 2  # Place child to the right, later in the row-major scan.
        parent = Cell(food=1000, x=10, y=10, genome=genome)
        world_grid[10][10] = parent

        calculate_surface()

        child = world_grid[10][11]
        self.assertIsInstance(child, Cell)
        self.assertIs(world_grid[10][10], parent)
        self.assertEqual(parent.count_of_life, 1)
        self.assertEqual(parent.count_of_cycle, 1)
        self.assertEqual(child.count_of_life, 0)
        self.assertEqual(child.count_of_cycle, 1)
        self.assertEqual(get_global_var("count_of_cells"), 1)


if __name__ == "__main__":
    unittest.main()
