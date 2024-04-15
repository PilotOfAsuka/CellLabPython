from pygame_init import *
import gui
from colors import BKG_COLOR
from simulation import update_surface, check_iterated


def pygame_cycle(run=False):
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            gui.start_stop_button.handle_event(event)
            gui.camera.handle_event(event)

        surface.fill(BKG_COLOR)
        gui.camera.update()

        #heck_iterated()

        #update_surface()
        gui.draw_gui()
        pg.display.flip()
        clock.tick(60)
