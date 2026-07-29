from dataclasses import dataclass

@dataclass
class Building:
    id: str
    x: float
    y: float
    width: float
    height: float

    def get_position(self):
        return (self.x, self.y)

    def get_bounds(self):
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height
        }