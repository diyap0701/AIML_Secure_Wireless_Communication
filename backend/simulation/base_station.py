from dataclasses import dataclass

@dataclass
class BaseStation:
    x: float
    y: float
    beam_direction: float = 0.0
    beam_width: float = 60.0

    def get_position(self):
        return (self.x, self.y)