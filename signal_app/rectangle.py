class Rectangle:
    def __init__(self, length: int, width: int):
        if not isinstance(length, int) or not isinstance(width, int):
            raise ValueError("Both length and width must be integers")
        if length <= 0 or width <= 0:
            raise ValueError("Length and width must be positive integers")
        self.length = length
        self.width = width
        self._index = 0  # To track iteration

    def __iter__(self):
        self._index = 0  # Reset iterator
        return self

    def __next__(self):
        if self._index == 0:
            self._index += 1
            return {'length': self.length}
        elif self._index == 1:
            self._index += 1
            return {'width': self.width}
        else:
            raise StopIteration

    def area(self):
        """Calculate area of rectangle."""
        return self.length * self.width

    def perimeter(self):
        """Calculate perimeter of rectangle."""
        return 2 * (self.length + self.width)
