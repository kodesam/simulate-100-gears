import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def create_gear(radius, teeth, center=(0, 0)):
    """
    Create the outline of a gear with specified radius, teeth, and center.
    """
    angles = np.linspace(0, 2 * np.pi, teeth * 2 + 1)
    gear_outline = []

    for i, angle in enumerate(angles):
        r = radius * (1.1 if i % 2 == 0 else 0.9)  # Alternate between "tooth" and "valley"
        x = center[0] + r * np.cos(angle)
        y = center[1] + r * np.sin(angle)
        gear_outline.append((x, y))

    return np.array(gear_outline)


def calculate_interlocking_gears(n_gears, base_radius, spacing):
    """
    Calculate the positions and sizes of 100 interlocking gears.
    """
    positions = []
    radii = []

    for i in range(n_gears):
        angle = i * 2 * np.pi / n_gears
        x = (base_radius + spacing) * np.cos(angle)
        y = (base_radius + spacing) * np.sin(angle)
        positions.append((x, y))
        radii.append(base_radius / (i + 1))  # Decrease radius for inner gears

    return positions, radii


class GearSimulation:
    def __init__(self, n_gears=100, base_radius=10, spacing=2):
        self.n_gears = n_gears
        self.base_radius = base_radius
        self.spacing = spacing
        self.positions, self.radii = calculate_interlocking_gears(n_gears, base_radius, spacing)

        self.gears = [
            create_gear(radius, teeth=15 + i * 2, center=pos)
            for i, (radius, pos) in enumerate(zip(self.radii, self.positions))
        ]

        self.fig, self.ax = plt.subplots()
        self.lines = []

        # Initialize lines for all gears
        for gear in self.gears:
            line, = self.ax.plot(gear[:, 0], gear[:, 1], lw=1)
            self.lines.append(line)

    def update(self, frame):
        """
        Update the gears' rotation for each animation frame.
        """
        for i, (gear, line) in enumerate(zip(self.gears, self.lines)):
            angle = frame / (i + 1)  # Inner gears rotate slower
            rotation_matrix = np.array([
                [np.cos(angle), -np.sin(angle)],
                [np.sin(angle), np.cos(angle)]
            ])
            rotated_gear = gear @ rotation_matrix.T
            line.set_data(rotated_gear[:, 0], rotated_gear[:, 1])

        return self.lines

    def run(self):
        """
        Run the gear simulation animation.
        """
        self.ax.axis("equal")
        self.ax.set_xlim(-self.base_radius * 3, self.base_radius * 3)
        self.ax.set_ylim(-self.base_radius * 3, self.base_radius * 3)
        self.ax.axis("off")

        anim = FuncAnimation(self.fig, self.update, frames=360, interval=20, blit=True)
        plt.show()


if __name__ == "__main__":
    sim = GearSimulation(n_gears=100, base_radius=10, spacing=2)
    sim.run()
