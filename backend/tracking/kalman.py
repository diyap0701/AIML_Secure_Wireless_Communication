import numpy as np
from filterpy.kalman import KalmanFilter


class WardenKalmanFilter:

    def __init__(self):

        self.kf = KalmanFilter(dim_x=4, dim_z=2)

        # State:
        # [x, y, vx, vy]
        self.kf.x = np.array([
            [0.0],
            [0.0],
            [0.0],
            [0.0]
        ])
        self.initialized = True
        # State transition matrix
        # Constant velocity model
        self.kf.F = np.array([
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=float)

        # Measurement matrix
        # Sensors only measure x and y
        self.kf.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], dtype=float)

        # Initial uncertainty
        self.kf.P *= 10

        # Process noise
        self.kf.Q *= 0.01

        # Measurement noise
        # We will change this depending on the sensor
        self.gps_R = np.array([
            [1.0, 0],
            [0, 1.0]
        ])

        self.camera_R = np.array([
            [0.16, 0],
            [0, 0.16]
        ])

    def predict(self):

        self.kf.predict()

    def update_gps(self, x, y):

        self.kf.R = self.gps_R

        measurement = np.array([
            [x],
            [y]
        ])

        self.kf.update(measurement)

    def update_camera(self, x, y):

        self.kf.R = self.camera_R

        measurement = np.array([
            [x],
            [y]
        ])

        self.kf.update(measurement)

    def get_state(self):

        x = self.kf.x[0, 0]
        y = self.kf.x[1, 0]

        vx = self.kf.x[2, 0]
        vy = self.kf.x[3, 0]

        return x, y, vx, vy