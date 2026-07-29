from dataclasses import dataclass

@dataclass
class Warden:
    x: float
    y: float

    def get_position(self):
        return (self.x, self.y)