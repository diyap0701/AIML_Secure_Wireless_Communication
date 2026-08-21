import math


class BeamManager:

    def __init__(self):
        self.current_beam_angle = 0
        self.current_beam_width = 60

    def calculate_beam_angle(self, warden_x, warden_y,
                             base_x, base_y):

        dx = warden_x - base_x
        dy = warden_y - base_y

        angle = math.degrees(math.atan2(dy, dx))

        if angle < 0:
            angle += 360

        return angle

    def adapt_beam(self, warden_x, warden_y,
                   base_x, base_y):

        angle = self.calculate_beam_angle(
            warden_x,
            warden_y,
            base_x,
            base_y
        )

        self.current_beam_angle = angle
        self.current_beam_width = 30

        return self.current_beam_angle, self.current_beam_width

    def normal_beam(self):

        self.current_beam_width = 60

        return (
            self.current_beam_angle,
            self.current_beam_width
        )

    def narrow_beam(self):

        self.current_beam_width = 15

        return (
            self.current_beam_angle,
            self.current_beam_width
        )