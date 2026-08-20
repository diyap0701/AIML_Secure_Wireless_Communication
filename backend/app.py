from simulation.environment import Environment
from simulation.base_station import BaseStation
from simulation.receiver import Receiver
from simulation.warden import Warden
from simulation.building import Building
from simulation.road import Road
from visualization.visualizer import Visualizer
from sensors.gps import GPSSensor
from sensors.camera import CameraSensor
from tracking.kalman import WardenKalmanFilter
from risk.risk_analyzer import RiskAnalyzer
from risk.risk_model import RiskModel
env = Environment(width=100, height=100)
gps = GPSSensor()
camera = CameraSensor()
kalman = WardenKalmanFilter()
base_station = BaseStation(x=10, y=35)
receiver = Receiver(x=45, y=45)
warden = Warden(
    x=10,
    y=22,
    speed=1,
    direction="right",
    current_road="R1"
)
risk_analyzer = RiskAnalyzer(
    base_station,
    receiver
)
gps = GPSSensor()
camera = CameraSensor()
risk_model = RiskModel()
env.set_base_station(base_station)
env.set_receiver(receiver)
env.set_warden(warden)

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
        x=50,
        y=0,
        width=4,
        height=100,
        direction="vertical"
    )
)

env.add_road(
    Road(
        id="R3",
        x=0,
        y=20,
        width=100,
        height=4,
        direction="horizontal"
    )
)

env.add_road(
    Road(
        id="R4",
        x=0,
        y=50,
        width=100,
        height=4,
        direction="horizontal"
    )
)

env.add_road(
    Road(
        id="R5",
        x=20,
        y=0,
        width=4,
        height=100,
        direction="vertical"
    )
)

env.add_road(
    Road(
        id="R6",
        x=35,
        y=0,
        width=4,
        height=100,
        direction="vertical"
    )
)
env.generate_intersections()
print(env.intersections)

visualizer = Visualizer(env)

for i in range(50):

    env.move_warden()

    intersection = env.get_current_intersection()

    true_x, true_y = env.warden.get_position()

    gps_x, gps_y = gps.measure(true_x, true_y)

    cam_x, cam_y = camera.measure(true_x, true_y)
    estimated_x = cam_x
    estimated_y = cam_y
    vx = 0
    vy = 0
    if not kalman.initialized:
        kalman.initialize(cam_x, cam_y)
    else:
        kalman.predict()
        kalman.update_gps(gps_x, gps_y)
        kalman.update_camera(cam_x, cam_y)

        estimated_x, estimated_y, vx, vy = kalman.get_state()
    movement_status, movement_value = risk_analyzer.movement_relative_to_path(
            estimated_x,
            estimated_y,
            vx,
            vy
        )
    distance = risk_analyzer.distance_from_transmission_path(
        estimated_x,
        estimated_y
    )
    risk_score, risk_level = risk_analyzer.calculate_risk(
    distance,movement_value,vx,vy
    )
    risk_score, risk_level = risk_model.calculate_risk(
    distance,
    movement_status,
    movement_value,
    (vx, vy),
    intersection
    )

   

    print("----------------------")

    print(
        "True      :",
        round(true_x, 2),
        round(true_y, 2)
    )

    if intersection:
        print("Intersection:", intersection)

    print(
        "GPS       :",
        round(gps_x, 2),
        round(gps_y, 2)
    )

    print(
        "Camera    :",
        round(cam_x, 2),
        round(cam_y, 2)
    )

    print(
        "Kalman    :",
        round(estimated_x, 2),
        round(estimated_y, 2)
    )

    print(
        "Velocity  :",
        round(vx, 2),
        round(vy, 2)
    )

    print(
        "Path Distance:",
        round(distance, 2)
    )

    print(
        "Movement     :",
        movement_status,
        round(movement_value, 2)
    )
    print(
    "Risk Score :", 
    round(risk_score, 2)
    )
    print(
        "Risk Level :", 
        risk_level
    )

    visualizer.draw()


import matplotlib.pyplot as plt

plt.ioff()
plt.show()