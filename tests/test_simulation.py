import unittest

from genome import Cell, Food
from misc import vars as v
from misc.func import get_global_var
from simulation import calculate_surface, restart_world, update_simulation


def reset_world():
    for y in range(v.GRID_SIZE_H):
        for x in range(v.GRID_SIZE_W):
            v.world_grid[y][x] = None
    v.active_objects.clear()
    v.global_vars.update({"count_of_cycle": 0, "count_of_food": 0, "count_of_cells": 0, "temp": 0})


class SimulationTests(unittest.TestCase):
    def setUp(self):
        reset_world()

    def test_paused_update_does_not_advance_cycle(self):
        update_simulation(is_running=False)

        self.assertEqual(get_global_var("count_of_cycle"), 0)

    def test_food_stays_in_place(self):
        food = Food(x=0, y=0)
        v.world_grid[0][0] = food
        v.register_object(food)

        calculate_surface()

        self.assertIs(v.world_grid[0][0], food)
        self.assertEqual(food.count_of_life, 1)
        self.assertEqual(food.count_of_cycle, 1)
        self.assertEqual(get_global_var("count_of_cycle"), 1)

    def test_newborn_cell_waits_until_next_cycle(self):
        genome = [0] * 64
        genome[1] = 2  # Place child to the right, later in the row-major scan.
        parent = Cell(food=1000, x=10, y=10, genome=genome)
        v.world_grid[10][10] = parent
        v.register_object(parent)

        calculate_surface()

        child = v.world_grid[10][11]
        self.assertIsInstance(child, Cell)
        self.assertIs(v.world_grid[10][10], parent)
        self.assertEqual(parent.count_of_life, 1)
        self.assertEqual(parent.count_of_cycle, 1)
        self.assertEqual(child.count_of_life, 0)
        self.assertEqual(child.count_of_cycle, 1)
        self.assertEqual(get_global_var("count_of_cells"), 1)

    def test_restart_world_rebuilds_size_and_genome_length(self):
        restart_world(cell_size=2, genome_size=80, start_cells=10)

        first_cell = next(obj for row in v.world_grid for obj in row if isinstance(obj, Cell))
        self.assertEqual(v.CELL_SIZE, 2)
        self.assertEqual(v.gen_size, 80)
        self.assertEqual(v.START_NUM_OF_CELL, 10)
        self.assertEqual(len(first_cell.genome), 80)

        restart_world(cell_size=3, genome_size=64, start_cells=1000)


if __name__ == "__main__":
    unittest.main()
