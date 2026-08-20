import math


class RiskAnalyzer:

    def __init__(self, base_station, receiver):

        self.base_station = base_station
        self.receiver = receiver
        self.previous_distance = None
    def get_closest_point_on_path(self, x, y):

        # Base Station
        x1 = self.base_station.x
        y1 = self.base_station.y

        # Receiver
        x2 = self.receiver.x
        y2 = self.receiver.y

        # BS -> Receiver vector
        dx = x2 - x1
        dy = y2 - y1

        # Warden relative to BS
        wx = x - x1
        wy = y - y1

        # Projection of Warden onto BS -> Receiver path
        t = (wx * dx + wy * dy) / (dx * dx + dy * dy)

        # Keep point inside actual BS -> Receiver segment
        t = max(0, min(1, t))

        # Closest point on transmission path
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        return closest_x, closest_y

    def distance_from_transmission_path(self, x, y):

        closest_x, closest_y = self.get_closest_point_on_path(x, y)

        distance = math.sqrt(
            (x - closest_x) ** 2 +
            (y - closest_y) ** 2
        )

        return distance

    def movement_relative_to_path(self, x, y, vx, vy):

        # Find closest point on transmission path
        closest_x, closest_y = self.get_closest_point_on_path(x, y)

        # Vector from Warden -> closest point on path
        direction_x = closest_x - x
        direction_y = closest_y - y

        distance = math.sqrt(
            direction_x ** 2 +
            direction_y ** 2
        )

        # Warden is already on the path
        if distance == 0:
            return "ON_PATH", 0.0

        # Normalize direction
        direction_x /= distance
        direction_y /= distance

        # Dot product between:
        # Warden velocity
        # and
        # direction toward path

        movement_towards_path = (
            vx * direction_x +
            vy * direction_y
        )

        # Threshold to avoid reacting to tiny noise
        threshold = 0.1

        if movement_towards_path > threshold:

            status = "APPROACHING"

        elif movement_towards_path < -threshold:

            status = "MOVING_AWAY"

        else:

            status = "PARALLEL"

        return status, movement_towards_path

    def calculate_risk(self, distance, movement, vx, vy):

        # ---------------- Distance Score ---------------- #

        if distance <= 2:
            distance_score = 70

        elif distance <= 5:
            distance_score = 50

        elif distance <= 10:
            distance_score = 30

        else:
            distance_score = 10


        # ---------------- Movement Score ---------------- #

        if movement == "APPROACHING":
            movement_score = 25

        elif movement == "PARALLEL":
            movement_score = 10

        elif movement == "MOVING_AWAY":
            movement_score = 0

        else:
            movement_score = 5


        # ---------------- Velocity Score ---------------- #

        speed = (vx ** 2 + vy ** 2) ** 0.5

        if movement == "APPROACHING" and speed > 1:
            velocity_score = 5
        else:
            velocity_score = 0


        # ---------------- Final Risk Score ---------------- #

        risk_score = distance_score + movement_score + velocity_score

        # Maximum = 100
        risk_score = min(risk_score, 100)


        # ---------------- Risk Level ---------------- #

        if risk_score >= 75:
            risk_level = "HIGH"

        elif risk_score >= 45:
            risk_level = "MEDIUM"

        else:
            risk_level = "LOW"


        return risk_score, risk_level