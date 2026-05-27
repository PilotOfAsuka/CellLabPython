import unittest

from genome import Cell, Food
from misc import environment
from misc import vars as v
from misc.func import get_global_var
from simulation import calculate_surface, restart_world, update_simulation


def reset_world():
    for y in range(v.GRID_SIZE_H):
        for x in range(v.GRID_SIZE_W):
            v.world_grid[y][x] = None
    v.active_objects.clear()
    v.bot_grid[:] = bytearray(v.GRID_SIZE_W * v.GRID_SIZE_H)
    v.neighbor_grid[:] = bytearray(v.GRID_SIZE_W * v.GRID_SIZE_H)
    environment.humidity_map = bytearray(v.GRID_SIZE_W * v.GRID_SIZE_H)
    environment.signal_map = bytearray(v.GRID_SIZE_W * v.GRID_SIZE_H)
    environment.active_signal_indexes.clear()
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
        v.set_bot_position(10, 10)
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

    def test_cell_leaves_signal(self):
        cell = Cell(x=3, y=3, genome=[55] * 64)
        v.world_grid[3][3] = cell
        v.set_bot_position(3, 3)
        v.register_object(cell)

        calculate_surface()

        self.assertGreater(environment.get_signal(3, 3), 0)

    def test_light_is_stronger_at_top(self):
        top_light = environment.get_light(0, 0, cycle=0)
        bottom_light = environment.get_light(0, v.GRID_SIZE_H - 1, cycle=0)

        self.assertGreater(top_light, bottom_light)

    def test_humidity_boosts_photosynthesis(self):
        dry_cell = Cell(food=500, x=5, y=5, genome=[0] * 64)
        v.world_grid[5][5] = dry_cell
        v.set_bot_position(5, 5)
        dry_cell.photosynthesis()
        dry_food = dry_cell.food

        reset_world()
        environment.humidity_map[environment.map_index(5, 5)] = 100
        wet_cell = Cell(food=500, x=5, y=5, genome=[0] * 64)
        v.world_grid[5][5] = wet_cell
        v.set_bot_position(5, 5)
        wet_cell.photosynthesis()

        self.assertGreater(wet_cell.food, dry_food)

    def test_signal_moves_genome_pointer(self):
        cell = Cell(x=4, y=4, genome=[1] * 64)
        v.world_grid[4][4] = cell
        v.set_bot_position(4, 4)
        signal_index = environment.map_index(4, 4)
        environment.signal_map[signal_index] = 60
        environment.active_signal_indexes.add(signal_index)

        cell.apply_environment_effects()

        self.assertNotEqual(cell.ptr, 0)

    def test_neighbor_grid_tracks_bots_not_food(self):
        cell = Cell(x=5, y=5, genome=[55] * 64)
        neighbor = Cell(x=6, y=5, genome=[55] * 64)
        food = Food(x=5, y=6)
        v.world_grid[5][5] = cell
        v.world_grid[5][6] = neighbor
        v.world_grid[6][5] = food
        v.set_bot_position(5, 5)
        v.set_bot_position(6, 5)

        self.assertEqual(cell.count_neighbors(), 1)

        v.world_grid[5][6] = None
        v.set_bot_position(6, 5, False)

        self.assertEqual(cell.count_neighbors(), 0)


if __name__ == "__main__":
    unittest.main()
