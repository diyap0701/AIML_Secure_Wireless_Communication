from dataclasses import dataclass

@dataclass
class Warden:
    x: float
    y: float
    speed: float
    direction: str
    current_road: str

    def get_position(self):
        return (self.x, self.y)