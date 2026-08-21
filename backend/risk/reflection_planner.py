import math


class ReflectionPlanner:

    def __init__(self, environment):
        self.environment = environment

    def distance(self, p1, p2):
        return math.sqrt(
            (p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2
        )

    def get_building_corners(self, building):

        return [
            (building.x, building.y),
            (building.x + building.width, building.y),
            (building.x, building.y + building.height),
            (
                building.x + building.width,
                building.y + building.height
            )
        ]

    def distance_point_to_segment(self, point, start, end):

        px, py = point
        x1, y1 = start
        x2, y2 = end

        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:
            return self.distance(point, start)

        t = (
            (px - x1) * dx +
            (py - y1) * dy
        ) / (dx * dx + dy * dy)

        t = max(0, min(1, t))

        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        return self.distance(
            point,
            (closest_x, closest_y)
        )

    def find_safe_reflection(self, warden_x, warden_y):

        bs = self.environment.base_station
        rx = self.environment.receiver

        warden = (warden_x, warden_y)
        base_station = (bs.x, bs.y)
        receiver = (rx.x, rx.y)

        SAFE_DISTANCE = 5

        candidates = []

        for building in self.environment.buildings:

            corners = self.get_building_corners(building)

            for corner in corners:

                bs_to_corner = self.distance(
                    base_station,
                    corner
                )

                corner_to_rx = self.distance(
                    corner,
                    receiver
                )

                total_path_length = (
                    bs_to_corner +
                    corner_to_rx
                )

                # Check whether Warden is close
                # to either reflected segment

                distance_to_first_segment = (
                    self.distance_point_to_segment(
                        warden,
                        base_station,
                        corner
                    )
                )

                distance_to_second_segment = (
                    self.distance_point_to_segment(
                        warden,
                        corner,
                        receiver
                    )
                )

                warden_clearance = min(
                    distance_to_first_segment,
                    distance_to_second_segment
                )

                if warden_clearance >= SAFE_DISTANCE:

                    candidates.append({
                        "point": corner,
                        "path_length": total_path_length,
                        "warden_clearance": warden_clearance
                    })

        if not candidates:
            return None

        # Prefer the shortest safe reflected path

        candidates.sort(
            key=lambda candidate: candidate["path_length"]
        )

        return candidates[0]