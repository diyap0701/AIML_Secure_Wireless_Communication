from dataclasses import dataclass

@dataclass
class Road:
    id: str
    x: float
    y: float
    width: float
    height: float
    direction: str

    def get_bounds(self):
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "direction": self.direction
        }