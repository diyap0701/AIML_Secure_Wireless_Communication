from .base_station import BaseStation
from .receiver import Receiver
from .warden import Warden
from .building import Building
from .road import Road

class Environment:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.base_station = None
        self.receiver = None
        self.warden = None
        self.buildings = []
        self.roads = []

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