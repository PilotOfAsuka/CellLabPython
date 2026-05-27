from pygame_init_graphic.pygame_init import pg
from misc import vars as v


class Camera:
    def __init__(self):
        # Камера хранит смещение в клетках мира, а renderer уже переводит его в пиксели.
        self.cam = pg.Rect(0, 0, v.width - v.gui_offset, v.height)
        self.scale = 1

        self.x_offset = 0
        self.y_offset = 0
        self.min_x_offset = 0
        self.min_y_offset = 0

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        # На масштабе 1 весь мир помещается в экран, поэтому смещение сбрасываем.
        if self.scale == 1:
            self.y_offset = 0
            self.x_offset = 0

        self.update_bounds()

        self.update_position()

    def update_bounds(self):
        viewport_w = v.width - v.gui_offset
        viewport_h = v.height
        cell_px = max(1, v.CELL_SIZE * self.scale)
        world_w = v.GRID_SIZE_W * cell_px
        world_h = v.GRID_SIZE_H * cell_px

        self.min_x_offset = -max(0, world_w - viewport_w) // cell_px
        self.min_y_offset = -max(0, world_h - viewport_h) // cell_px
        self.x_offset = self.clamp_offset(self.x_offset, self.min_x_offset)
        self.y_offset = self.clamp_offset(self.y_offset, self.min_y_offset)

    def clamp_offset(self, value, min_offset):
        return max(min_offset, min(0, value))

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_PLUS or event.key == pg.K_EQUALS:
                self.scale = self.scale + 1 if -1 < self.scale + 1 < 4 else self.scale
            elif event.key == pg.K_MINUS:
                self.scale = self.scale - 1 if 0 < self.scale - 1 < 4 else self.scale

            elif event.key == pg.K_LEFT:
                self.moving_left = True
                pass
            elif event.key == pg.K_UP:
                self.moving_up = True
                pass
            elif event.key == pg.K_RIGHT:
                self.moving_right = True
                pass
            elif event.key == pg.K_DOWN:
                self.moving_down = True
                pass
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                self.moving_left = False
                pass
            elif event.key == pg.K_UP:
                self.moving_up = False
                pass
            elif event.key == pg.K_RIGHT:
                self.moving_right = False
                pass
            elif event.key == pg.K_DOWN:
                self.moving_down = False
                pass

    def update_position(self):
        if self.moving_left is True:
            self.x_offset = self.clamp_offset(self.x_offset + 1, self.min_x_offset)

        if self.moving_right is True:
            self.x_offset = self.clamp_offset(self.x_offset - 1, self.min_x_offset)

        if self.moving_up is True:
            self.y_offset = self.clamp_offset(self.y_offset + 1, self.min_y_offset)
            pass
        if self.moving_down is True:
            self.y_offset = self.clamp_offset(self.y_offset - 1, self.min_y_offset)
            pass


camera = Camera()
