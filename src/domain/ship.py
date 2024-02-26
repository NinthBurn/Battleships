class Battleship:
    def __init__(self, x, y, size, vertical):
        self.x = x
        self.y = y
        self.size = size
        self.vertical = vertical

    def __eq__(self, com):
        return (self.x == com.x and self.y == com.y and self.size == com.size and self.vertical == com.vertical)
