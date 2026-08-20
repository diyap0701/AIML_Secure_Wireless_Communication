import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class Visualizer:

    def __init__(self, environment):
        self.environment = environment

        plt.ion()                         # Interactive mode
        self.fig, self.ax = plt.subplots(figsize=(8,8))


    def draw(self):

        self.ax.clear()

        self.ax.set_xlim(0, self.environment.width)
        self.ax.set_ylim(0, self.environment.height)

        self.ax.set_title("Adaptive Beam Management Simulation")
        self.ax.set_xlabel("X Coordinate")
        self.ax.set_ylabel("Y Coordinate")

        # ---------------- Roads ---------------- #

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

        # ---------------- Buildings ---------------- #

        for building in self.environment.buildings:

            self.ax.add_patch(

                Rectangle(

                    (building.x, building.y),

                    building.width,

                    building.height,

                    color="brown"

                )

            )

        # ---------------- Base Station ---------------- #

        bs = self.environment.base_station

        self.ax.scatter(

            bs.x,

            bs.y,

            color="blue",

            s=120,

            label="Base Station"

        )

        # ---------------- Receiver ---------------- #

        rx = self.environment.receiver

        self.ax.scatter(

            rx.x,

            rx.y,

            color="green",

            s=120,

            label="Receiver"

        )

        # ---------------- Warden ---------------- #

        w = self.environment.warden

        self.ax.scatter(

            w.x,

            w.y,

            color="red",

            s=120,

            label="Warden"

        )

        self.ax.grid(True)

        self.ax.legend()

        plt.pause(0.05)      