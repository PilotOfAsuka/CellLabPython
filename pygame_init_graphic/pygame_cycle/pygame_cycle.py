from pygame_init_graphic.pygame_init import *
from pygame_init_graphic.gui import draw_gui, start_stop_button, draw_button
from camera.camera import camera
from misc.colors import BKG_COLOR
from simulation import update_surface, draw_surface
from simulation_test import test_init_cells,test_draw_surface,test_update_surface
from misc.vars import FPS
import threading
from genome_class.init_new_genome import init_cells


#init_cells()

test_init_cells()


def logic_thread():
    while True:
        test_update_surface()
        #time.sleep(1/120)  # Логика обновляется 60 раз в секунду

thread = threading.Thread(target=logic_thread, daemon=True)
thread.start()

def start_cycle(run=False):
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            start_stop_button.handle_event(event)
            draw_button.handle_event(event)
            camera.handle_event(event)

        surface.fill(BKG_COLOR)
        camera.update()

        #update_surface()
        test_draw_surface()

        draw_gui()
        pg.display.flip()
        clock.tick(FPS)

