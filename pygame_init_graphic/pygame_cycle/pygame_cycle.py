from pygame_init_graphic.pygame_init import *
from pygame_init_graphic.gui import draw_gui, start_stop_button
from camera.camera import camera
from misc.colors import BKG_COLOR
from simulation import update_surface, draw_surface, init_cells
from misc.func import set_global_var, get_global_var, weather_simulation
from misc.vars import FPS

init_cells()


def start_cycle(run=False):
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            start_stop_button.handle_event(event)
            camera.handle_event(event)

        surface.fill(BKG_COLOR)
        camera.update()

        set_global_var(var="temp", value=weather_simulation(get_global_var("count_of_cycle")))
        update_surface()
        draw_surface()

        draw_gui()
        pg.display.flip()
        clock.tick(FPS)
