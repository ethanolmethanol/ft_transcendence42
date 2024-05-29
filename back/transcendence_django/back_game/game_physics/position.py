class Position:
    def __init__(self, x:float=0, y:float=0):
        self.x: float = x
        self.y: float = y

    def set_coordinates(self, x: float, y: float):
        self.x = x
        self.y = y

    def round(self) -> 'Position':
        self.x = round(self.x)
        self.y = round(self.y)
        return self

