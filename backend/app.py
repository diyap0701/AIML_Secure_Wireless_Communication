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
from communication.decision_engine import CommunicationDecisionEngine
from communication.beam_manager import BeamManager
from risk.reflection_planner import ReflectionPlanner

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
decision_engine = CommunicationDecisionEngine()
beam_manager = BeamManager()
decision = decision_engine.decide(risk_model)
reflection_planner = ReflectionPlanner(env)

env.add_building(
    Building(
        id="B1",
        x=42,
        y=10,
        width=8,
        height=8
    )
)

env.add_building(
    Building(
        id="B2",
        x=41,
        y=60,
        width=8,
        height=8
    )
)
env.add_building(
    Building(
        id="B3",
        x=3,
        y=60,
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
current_strategy = "BEAM_WIDE"
for i in range(29):

    env.move_warden()

    intersection = env.get_current_intersection()

    true_x, true_y = env.warden.get_position()

    gps_x, gps_y = gps.measure(true_x, true_y)

    cam_x, cam_y = camera.measure(true_x, true_y)

    # ---------------- Kalman Filter ---------------- #

    if not kalman.initialized:

        kalman.initialize(cam_x, cam_y)

        estimated_x = cam_x
        estimated_y = cam_y
        vx = 0
        vy = 0

    else:

        kalman.predict()

        kalman.update_gps(gps_x, gps_y)

        kalman.update_camera(cam_x, cam_y)

        estimated_x, estimated_y, vx, vy = kalman.get_state()

    # ---------------- Risk Analysis ---------------- #

    distance = risk_analyzer.distance_from_transmission_path(
        estimated_x,
        estimated_y
    )

    movement_status, movement_value = (
        risk_analyzer.movement_relative_to_path(
            estimated_x,
            estimated_y,
            vx,
            vy
        )
    )

    # ---------------- Risk Score ---------------- #

    risk_score, risk_level = risk_analyzer.calculate_risk(
        distance,
        movement_status,
        vx,
        vy
    )
    # Find possible safe reflected path
    reflection = reflection_planner.find_safe_reflection(
        estimated_x,
        estimated_y
    )
    # ---------------- Dynamic Beam Strategy ---------------- #

    if distance <= 2:

        if reflection:
            current_strategy = "REFLECTION"
        else:
            current_strategy = "BEAM_NARROW"

    elif distance <= 5:

        if current_strategy != "REFLECTION":
            current_strategy = "BEAM_NARROW"

    else:

        if current_strategy != "REFLECTION":
            current_strategy = "BEAM_WIDE"


    decision = current_strategy


    # ---------------- Beam Parameters ---------------- #

    if decision == "BEAM_WIDE":

        beam_angle = 0
        beam_width = 60

    elif decision == "BEAM_NARROW":

        beam_angle = 0
        beam_width = 20

    elif decision == "REFLECTION":

        beam_angle = 0
        beam_width = 10

    else:

        beam_angle = 0
        beam_width = 60

    # ---------------- Reflection ---------------- #

    reflection = reflection_planner.find_safe_reflection(
        estimated_x,
        estimated_y
    )

    # ---------------- Printing ---------------- #

    print("----------------------")

    print(
        "True      :",
        round(true_x, 2),
        round(true_y, 2)
    )

    if intersection:
        print(
            "Intersection:",
            intersection
        )

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
        "Risk Score   :",
        round(risk_score, 2)
    )

    print(
        "Risk Level   :",
        risk_level
    )

    print(
        "Decision     :",
        decision
    )

    print(
        "Beam Angle   :",
        round(beam_angle, 2)
    )

    print(
        "Beam Width   :",
        round(beam_width, 2)
    )

    # ---------------- Reflection Information ---------------- #

    if reflection:

        print(
            "Safe Reflection Point:",
            reflection["point"]
        )

        print(
            "Reflected Path Length:",
            round(
                reflection["path_length"],
                2
            )
        )

        print(
            "Warden Clearance:",
            round(
                reflection["warden_clearance"],
                2
            )
        )

    else:

        print(
            "Safe Reflection: NOT AVAILABLE"
        )

    # ---------------- Visualization ---------------- #

    visualizer.set_transmission_state(
        decision,
        risk_level,
        reflection["point"] if reflection else None
    )

    visualizer.draw()


# Keep window open after simulation
import matplotlib.pyplot as plt

plt.ioff()
plt.show()