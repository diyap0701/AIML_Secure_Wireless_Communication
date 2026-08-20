import random
class CameraSensor:
    def __init__(self, noise_std=0.4):
        self.noise_std = noise_std

    def measure(self, true_x, true_y):

        measured_x = true_x + random.gauss(0, self.noise_std)
        measured_y = true_y + random.gauss(0, self.noise_std)

        return measured_x, measured_y