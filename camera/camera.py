from pygame_init_graphic.pygame_init import pg
from misc.vars import width, height


class Camera:
    def __init__(self):
        self.cam = pg.Rect(0, 0, width-200, height)
        self.scale = 1

        self.x_offset = 0
        self.y_offset = 0
        self.min_offset = 0

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        # Обновление камеры
        if self.scale == 1:
            self.y_offset = 0
            self.x_offset = 0

        if self.scale == 2:
            self.min_offset = -100
        elif self.scale == 3:
            self.min_offset = -133

        self.update_position()

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
            self.x_offset = self.x_offset + 1 if self.min_offset < self.x_offset + 1 < 1 else self.x_offset

        if self.moving_right is True:
            self.x_offset = self.x_offset - 1 if self.min_offset < self.x_offset - 1 < 1 else self.x_offset

        if self.moving_up is True:
            self.y_offset = self.y_offset + 1 if self.min_offset < self.y_offset + 1 < 1 else self.y_offset
            pass
        if self.moving_down is True:
            self.y_offset = self.y_offset - 1 if self.min_offset < self.y_offset - 1 < 1 else self.y_offset
            pass


camera = Camera()
