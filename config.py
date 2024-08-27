import ctypes

class Config:
    def __init__(self) -> None:
        self.width = ctypes.windll.user32.GetSystemMetrics(0)
        self.height = ctypes.windll.user32.GetSystemMetrics(1)
        self.margin = 16
        self.rows = 5
        self.columns = 5
        self.length_win = 4
        self.tile_size = (self.height - 2 * self.margin) // self.rows
        self.strike4 = True
        self.debug = False