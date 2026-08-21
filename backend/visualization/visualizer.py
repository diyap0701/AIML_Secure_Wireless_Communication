import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math


class Visualizer:

    def __init__(self, environment):

        self.environment = environment

        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(8, 8))

        # Current transmission state
        self.decision = "BEAM_WIDE"
        self.risk_level = "LOW"
        self.reflection_point = None

    # --------------------------------------------------
    # RECEIVE CURRENT TRANSMISSION STATE
    # --------------------------------------------------

    def set_transmission_state(
        self,
        decision,
        risk_level,
        reflection_point=None
    ):

        self.decision = decision
        self.risk_level = risk_level
        self.reflection_point = reflection_point

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------

    def draw(self):

        self.ax.clear()

        self.ax.set_xlim(
            0,
            self.environment.width
        )

        self.ax.set_ylim(
            0,
            self.environment.height
        )

        self.ax.set_title(
            "Adaptive Beam Management Simulation"
        )

        self.ax.set_xlabel("X Coordinate")
        self.ax.set_ylabel("Y Coordinate")

        # --------------------------------------------------
        # ROADS
        # --------------------------------------------------

        for road in self.environment.roads:

            self.ax.add_patch(

                Rectangle(

                    (road.x, road.y),

                    road.width,
                    road.height,

                    color="gray",
                    alpha=0.5

                )

            )

        # --------------------------------------------------
        # BUILDINGS
        # --------------------------------------------------

        for building in self.environment.buildings:

            self.ax.add_patch(

                Rectangle(

                    (building.x, building.y),

                    building.width,
                    building.height,

                    color="brown"

                )

            )

        # --------------------------------------------------
        # BASE STATION
        # --------------------------------------------------

        bs = self.environment.base_station

        self.ax.scatter(

            bs.x,
            bs.y,

            color="blue",
            s=120,

            label="Base Station"

        )

        # --------------------------------------------------
        # RECEIVER
        # --------------------------------------------------

        rx = self.environment.receiver

        self.ax.scatter(

            rx.x,
            rx.y,

            color="green",
            s=120,

            label="Receiver"

        )

        # --------------------------------------------------
        # WARDEN
        # --------------------------------------------------

        w = self.environment.warden

        self.ax.scatter(

            w.x,
            w.y,

            color="red",
            s=120,

            label="Warden"

        )

        # --------------------------------------------------
        # TRANSMISSION
        # --------------------------------------------------

        if self.decision == "REFLECTION":

            self.draw_reflected_transmission()

        else:

            self.draw_direct_transmission()

        # --------------------------------------------------
        # STATUS TEXT
        # --------------------------------------------------

        self.ax.text(

            2,
            96,

            f"Mode: {self.decision}",

            fontsize=11,
            fontweight="bold"

        )

        self.ax.text(

            2,
            92,

            f"Risk: {self.risk_level}",

            fontsize=10

        )

        self.ax.grid(True)

        self.ax.legend()

        plt.pause(0.05)

    # --------------------------------------------------
    # DIRECT TRANSMISSION
    # --------------------------------------------------

    def draw_direct_transmission(self):

        bs = self.environment.base_station
        rx = self.environment.receiver

        # -----------------------------
        # Main transmission line
        # -----------------------------

        self.ax.plot(

            [bs.x, rx.x],

            [bs.y, rx.y],

            linewidth=4,

            label="Direct Transmission"

        )

        # -----------------------------
        # Beam width
        # -----------------------------

        if self.decision == "BEAM_WIDE":

            beam_width = 60

        elif self.decision == "BEAM_NARROW":

            beam_width = 20

        else:

            beam_width = 60

        # Convert beam width into a visual
        # perpendicular offset

        dx = rx.x - bs.x
        dy = rx.y - bs.y

        length = math.sqrt(
            dx ** 2 +
            dy ** 2
        )

        if length == 0:
            return

        # Perpendicular unit vector

        px = -dy / length
        py = dx / length

        # Visual scaling

        offset = beam_width / 10

        # Upper beam boundary

        upper_x = [
            bs.x + px * offset,
            rx.x + px * offset
        ]

        upper_y = [
            bs.y + py * offset,
            rx.y + py * offset
        ]

        # Lower beam boundary

        lower_x = [
            bs.x - px * offset,
            rx.x - px * offset
        ]

        lower_y = [
            bs.y - py * offset,
            rx.y - py * offset
        ]

        self.ax.plot(

            upper_x,
            upper_y,

            linestyle="--",
            linewidth=1.5

        )

        self.ax.plot(

            lower_x,
            lower_y,

            linestyle="--",
            linewidth=1.5

        )

    # --------------------------------------------------
    # REFLECTED TRANSMISSION
    # --------------------------------------------------

    def draw_reflected_transmission(self):

        bs = self.environment.base_station

        rx = self.environment.receiver

        point = self.reflection_point

        # Safety check

        if point is None:

            self.draw_direct_transmission()

            return

        reflection_x = point[0]
        reflection_y = point[1]

        # --------------------------------------------------
        # BS -> BUILDING
        # --------------------------------------------------

        self.ax.plot(

            [bs.x, reflection_x],

            [bs.y, reflection_y],

            linewidth=4,

            label="Reflected Transmission"

        )

        # --------------------------------------------------
        # BUILDING -> RECEIVER
        # --------------------------------------------------

        self.ax.plot(

            [reflection_x, rx.x],

            [reflection_y, rx.y],

            linewidth=4

        )

        # --------------------------------------------------
        # REFLECTION POINT
        # --------------------------------------------------

        self.ax.scatter(

            reflection_x,
            reflection_y,

            color="orange",

            s=100,

            marker="X",

            label="Reflection Point"

        )

        # --------------------------------------------------
        # SMALL INDICATOR
        # --------------------------------------------------

        self.ax.text(

            reflection_x + 1,
            reflection_y + 1,

            "REFLECTION",

            fontsize=9,
            fontweight="bold"

        )