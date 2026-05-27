from camera.camera import camera
from misc import colors as c
from misc import vars as v
from misc.func import get_global_var, set_global_var
from pygame_init_graphic.pygame_init import clock, font, pg, surface


# GUI читает состояние симуляции и меняет только настройки. Мир пересоздается через restart_world().
PANEL_X = v.width - v.gui_offset
PANEL_PADDING = 18
PANEL_WIDTH = v.gui_offset
PANEL_COLOR = 117, 104, 84
BUTTON_BORDER = 42, 42, 42
BUTTON_COLOR = 72, 83, 89
BUTTON_HOVER = 92, 106, 112


def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)


def render_text(text, x, y, color=c.WHITE):
    text_surface = font.render(str(text), True, color)
    surface.blit(text_surface, (x, y))
    return text_surface.get_rect(topleft=(x, y))


def draw_panel_row(label, value, y):
    render_text(f"{label}: {value}", PANEL_X + PANEL_PADDING, y)


def format_ms(value):
    value = 0 if value is None else value
    return f"{value:.2f}"


class TextButton:
    def __init__(self, x, y, w, h, text, callback=None, color=BUTTON_COLOR, hover_color=BUTTON_HOVER):
        self.rect = pg.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.color = color
        self.hover_color = hover_color

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            if self.callback is not None:
                self.callback()
            return True
        return False

    def draw(self, text=None, color=None):
        label = self.text if text is None else text
        mouse_pos = pg.mouse.get_pos()
        fill_color = color or (self.hover_color if self.rect.collidepoint(mouse_pos) else self.color)
        pg.draw.rect(surface, fill_color, self.rect, border_radius=5)
        pg.draw.rect(surface, BUTTON_BORDER, self.rect, width=2, border_radius=5)

        text_surface = font.render(label, True, c.WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class RunButton(TextButton):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, "STOP")
        self.click = True

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            self.click = not self.click
            return True
        return False

    def draw(self):
        if self.click:
            super().draw("STOP", color=(170, 24, 55))
        else:
            super().draw("PLAY", color=(25, 140, 62))


class NumberSetting:
    def __init__(self, label, key, x, y, min_value, max_value, step):
        self.label = label
        self.key = key
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.minus_button = TextButton(x + 390, y, 44, 38, "-", self.decrease)
        self.plus_button = TextButton(x + 440, y, 44, 38, "+", self.increase)
        self.x = x
        self.y = y

    def value(self):
        return int(get_global_var(self.key))

    def set_value(self, value):
        set_global_var(self.key, clamp(value, self.min_value, self.max_value))

    def decrease(self):
        self.set_value(self.value() - self.step)

    def increase(self):
        self.set_value(self.value() + self.step)

    def handle_event(self, event):
        return self.minus_button.handle_event(event) or self.plus_button.handle_event(event)

    def draw(self):
        render_text(f"{self.label}: {self.value()}", self.x, self.y)
        self.minus_button.draw()
        self.plus_button.draw()


class SettingsWindow:
    def __init__(self):
        self.is_open = False
        self.rect = pg.Rect(90, 55, v.width - 180, v.height - 110)
        self.close_button = TextButton(self.rect.right - 64, self.rect.y + 18, 44, 38, "X", self.close)
        left_x = self.rect.x + 32
        self.temp_button = TextButton(left_x + 390, self.rect.y + 126, 150, 38, "TEMP", self.toggle_temp)
        self.cell_size = NumberSetting("Cell size", "cell_size_setting", left_x, self.rect.y + 200, 1, 20, 1)
        self.genome_size = NumberSetting("Genome size", "genome_size_setting", left_x, self.rect.y + 256, 16, 256, 8)
        self.start_cells = NumberSetting("Start cells", "start_cells_setting", left_x, self.rect.y + 312,
                                         1, max(1, (v.width - v.gui_offset) * v.height), 100)
        self.restart_button = TextButton(left_x, self.rect.y + 390, 360, 44, "RESTART WORLD", self.restart_world,
                                         color=(25, 125, 84), hover_color=(35, 145, 98))

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def toggle(self):
        self.is_open = not self.is_open

    def toggle_temp(self):
        set_global_var("temp_running", not bool(get_global_var("temp_running")))

    def restart_world(self):
        from simulation import restart_world

        restart_world(
            cell_size=get_global_var("cell_size_setting"),
            genome_size=get_global_var("genome_size_setting"),
            start_cells=get_global_var("start_cells_setting"),
        )
        camera.scale = 1
        camera.x_offset = 0
        camera.y_offset = 0

    def handle_event(self, event):
        if not self.is_open:
            return False

        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.close()
            return True

        buttons = (self.close_button, self.temp_button, self.restart_button)
        for button in buttons:
            if button.handle_event(event):
                return True

        for setting in (self.cell_size, self.genome_size, self.start_cells):
            if setting.handle_event(event):
                return True

        # Пока окно открыто, клики внутри него не должны проваливаться в камеру.
        if event.type == pg.MOUSEBUTTONDOWN:
            return True
        return False

    def draw(self):
        if not self.is_open:
            return

        dim_surface = pg.Surface((v.width, v.height), pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 96))
        surface.blit(dim_surface, (0, 0))

        pg.draw.rect(surface, (84, 91, 82), self.rect, border_radius=6)
        pg.draw.rect(surface, c.BLACK, self.rect, width=2, border_radius=6)
        render_text("SETTINGS", self.rect.x + 28, self.rect.y + 20)
        self.close_button.draw()

        temp_label = "PLAY" if get_global_var("temp_running") else "PAUSE"
        render_text(f"Temperature: {temp_label}", self.rect.x + 32, self.rect.y + 128)
        self.temp_button.draw(temp_label, color=(25, 140, 62) if get_global_var("temp_running") else (170, 24, 55))

        self.cell_size.draw()
        self.genome_size.draw()
        self.start_cells.draw()
        self.restart_button.draw()

        render_text("ABOUT", self.rect.x + 650, self.rect.y + 126)
        render_text("CellLab Python", self.rect.x + 650, self.rect.y + 180)
        render_text("Restart rebuilds layers.", self.rect.x + 650, self.rect.y + 234)
        render_text(f"Current grid: {v.GRID_SIZE_W} x {v.GRID_SIZE_H}", self.rect.x + 650, self.rect.y + 288)


settings_window = SettingsWindow()

start_stop_button = RunButton(PANEL_X + PANEL_PADDING, 356, PANEL_WIDTH - PANEL_PADDING * 2, 44)
settings_button = TextButton(PANEL_X + PANEL_PADDING, 410, PANEL_WIDTH - PANEL_PADDING * 2, 44,
                             "SETTINGS", settings_window.toggle)
restart_button = TextButton(PANEL_X + PANEL_PADDING, 464, PANEL_WIDTH - PANEL_PADDING * 2, 44,
                            "RESTART", settings_window.restart_world,
                            color=(25, 125, 84), hover_color=(35, 145, 98))


def handle_gui_event(event):
    if settings_window.handle_event(event):
        return True
    for button in (settings_button, restart_button, start_stop_button):
        if button.handle_event(event):
            return True
    return False


def draw_gui_rect():
    rect = pg.Rect(PANEL_X, 0, PANEL_WIDTH, v.height)
    pg.draw.rect(surface, PANEL_COLOR, rect)


def draw_border():
    rect = pg.Rect(0, 0, v.width - v.gui_offset, v.height)
    pg.draw.rect(surface, c.BLACK, rect, width=2)


def draw_gui():
    draw_gui_rect()

    draw_panel_row("Cells", get_global_var("count_of_cells"), 12)
    draw_panel_row("Organic", get_global_var("count_of_food"), 52)
    draw_panel_row("Cycle", get_global_var("count_of_cycle"), 92)
    draw_panel_row("Temp", get_global_var("temp"), 132)
    draw_panel_row("Sim ms", format_ms(get_global_var("simulation_ms")), 172)
    draw_panel_row("Draw ms", format_ms(get_global_var("draw_ms")), 212)
    draw_panel_row("Rects", get_global_var("drawn_objects"), 252)
    draw_panel_row("FPS", int(clock.get_fps()), 292)

    start_stop_button.draw()
    settings_button.draw()
    restart_button.draw()
    draw_border()
    settings_window.draw()
