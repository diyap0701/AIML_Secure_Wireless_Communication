from simulation.environment import Environment
from simulation.base_station import BaseStation
from simulation.receiver import Receiver
from simulation.warden import Warden
from simulation.building import Building
from simulation.road import Road

# Create environment
env = Environment(width=100, height=100)

# Create entities
base_station = BaseStation(x=10, y=10)
receiver = Receiver(x=90, y=80)
warden = Warden(x=10, y=40)

# Add entities to environment
env.set_base_station(base_station)
env.set_receiver(receiver)
env.set_warden(warden)

# Add buildings
env.add_building(
    Building(
        id="B1",
        x=15,
        y=10,
        width=12,
        height=12
    )
)

env.add_building(
    Building(
        id="B2",
        x=45,
        y=50,
        width=15,
        height=15
    )
)

# Add roads
env.add_road(
    Road(
        id="R1",
        x=0,
        y=38,
        width=100,
        height=4,
        direction="horizontal"
    )
)

env.add_road(
    Road(
        id="R2",
        x=72,
        y=0,
        width=4,
        height=100,
        direction="vertical"
    )
)

# Print current state
print(env.get_state())