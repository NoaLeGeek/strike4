import ctypes

class Config:
    def __init__(self) -> None:
        self.width = ctypes.windll.user32.GetSystemMetrics(0)
        self.height = ctypes.windll.user32.GetSystemMetrics(1)
        self.rows = 5
        self.columns = 5
        self.length_win = 4
        self.debug = False