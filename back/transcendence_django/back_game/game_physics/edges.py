class Edges:
    def __init__(self, position, width, height):
        self.update(position, width, height)

    def update(self, position, width, height):
        self.bottom = position.y + height / 2
        self.top = position.y - height / 2
        self.left = position.x - width / 2
        self.right = position.x + width / 2
