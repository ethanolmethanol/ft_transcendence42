class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def setCoordinates(self, x, y):
        self.x = x
        self.y = y

    def round(self):
        self.x = round(self.x)
        self.y = round(self.y)
        return self

    def to_dict(self):
        return {"x": self.x, "y": self.y}
