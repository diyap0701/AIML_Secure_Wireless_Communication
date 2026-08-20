from .base_station import BaseStation
from .receiver import Receiver
from .warden import Warden
from .building import Building
from .road import Road
import random

class Environment:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.base_station = None
        self.receiver = None
        self.warden = None
        self.buildings = []
        self.roads = []
        self.intersections = []

    def set_base_station(self, base_station: BaseStation):
        self.base_station = base_station

    def set_receiver(self, receiver: Receiver):
        self.receiver = receiver

    def set_warden(self, warden: Warden):
        self.warden = warden

    def add_building(self, building: Building):
        self.buildings.append(building)

    def add_road(self, road: Road):
        self.roads.append(road)

    def get_state(self):
        return {
            "base_station": self.base_station.get_position() if self.base_station else None,
            "receiver": self.receiver.get_position() if self.receiver else None,
            "warden": self.warden.get_position() if self.warden else None,

            "buildings": [
                building.get_bounds()
                for building in self.buildings
            ],

            "roads": [
                road.get_bounds()
                for road in self.roads
            ]
        }
    def move_warden(self):

        if self.warden is None:
            return

        # Check if the warden is at an intersection
        intersection = self.get_current_intersection()

        if intersection:
            next_move = self.choose_next_road(intersection)

            self.warden.current_road = next_move["road"]
            self.warden.direction = next_move["direction"]

        road = self.get_road_by_id(self.warden.current_road)

        if road is None:
            return

        if road.direction == "horizontal":

            # Keep the warden on the center of the road
            self.warden.y = road.y + (road.height / 2)

            if self.warden.direction == "right":
                self.warden.x += self.warden.speed

            elif self.warden.direction == "left":
                self.warden.x -= self.warden.speed

        elif road.direction == "vertical":

            # Keep the warden on the center of the road
            self.warden.x = road.x + (road.width / 2)

            if self.warden.direction == "up":
                self.warden.y += self.warden.speed

            elif self.warden.direction == "down":
                self.warden.y -= self.warden.speed
    def generate_intersections(self):

        self.intersections = []

        horizontal_roads = [
            road for road in self.roads
            if road.direction == "horizontal"
        ]

        vertical_roads = [
            road for road in self.roads
            if road.direction == "vertical"
        ]

        for h in horizontal_roads:
            for v in vertical_roads:

                intersection = {
                    "x": v.x + v.width / 2,
                    "y": h.y + h.height / 2,
                    "horizontal": h.id,
                    "vertical": v.id
                }

                self.intersections.append(intersection)
    def get_current_intersection(self, tolerance=0.5):

        if self.warden is None:
            return None

        for intersection in self.intersections:
            if (
                abs(self.warden.x - intersection["x"]) <= tolerance
                and
                abs(self.warden.y - intersection["y"]) <= tolerance
            ):
                return intersection
        return None
    def get_possible_turns(self, intersection):

        possible_turns = []

        current_road = self.get_road_by_id(self.warden.current_road)

        if current_road.direction == "horizontal":

            # Continue straight
            possible_turns.append({
                "road": current_road.id,
                "direction": self.warden.direction
            })

            # Turn onto the vertical road
            vertical_road = intersection["vertical"]

            if self.warden.direction == "right":

                possible_turns.append({
                    "road": vertical_road,
                    "direction": "up"
                })

                possible_turns.append({
                    "road": vertical_road,
                    "direction": "down"
                })

            else:   # moving left

                possible_turns.append({
                    "road": vertical_road,
                    "direction": "up"
                })

                possible_turns.append({
                    "road": vertical_road,
                    "direction": "down"
                })

        else:

            # Continue straight
            possible_turns.append({
                "road": current_road.id,
                "direction": self.warden.direction
            })

            horizontal_road = intersection["horizontal"]

            if self.warden.direction == "up":

                possible_turns.append({
                    "road": horizontal_road,
                    "direction": "left"
                })

                possible_turns.append({
                    "road": horizontal_road,
                    "direction": "right"
                })

            else:

                possible_turns.append({
                    "road": horizontal_road,
                    "direction": "left"
                })

                possible_turns.append({
                    "road": horizontal_road,
                    "direction": "right"
                })

        return possible_turns
    def choose_next_road(self, intersection):

        possible_turns = self.get_possible_turns(intersection)

        return random.choice(possible_turns)
    def get_road_by_id(self, road_id):
        for road in self.roads:
            if road.id == road_id:
                return road
        return None