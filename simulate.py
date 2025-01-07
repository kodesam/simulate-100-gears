import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import streamlit as st

def create_gear(radius, teeth, center=(0, 0)):
    angles = np.linspace(0, 2 * np.pi, teeth * 2 + 1)
    gear_outline = []
    for i, angle in enumerate(angles):
        r = radius * (1.1 if i % 2 == 0 else 0.9)
        x = center[0] + r * np.cos(angle)
        y = center[1] + r * np.sin(angle)
        gear_outline.append((x, y))
    return np.array(gear_outline)

class GearReductionSimulation:
    def __init__(self, n_gears=100, initial_radius=10, gear_ratio=10, spacing=12):
        self.n_gears = n_gears
        self.gear_ratio = gear_ratio
        self.spacing = spacing
        self.positions = [(i * spacing, 0) for i in range(n_gears)]
        self.radii = [initial_radius / (gear_ratio**i) for i in range(n_gears)]
        self.teeth = [int(15 * (gear_ratio**i)) for i in range(n_gears)]
        self.gears = [
            create_gear(radius, teeth, center=pos)
            for radius, teeth, pos in zip(self.radii, self.teeth, self.positions)
        ]
        self.fig, self.ax = plt.subplots()
        self.lines = []
        for gear in self.gears:
            line, = self.ax.plot(gear[:, 0], gear[:, 1], lw=1, color='gray')
            self.lines.append(line)
        self.ax.axis("equal")
        self.ax.axis("off")

    def update(self, frame):
        driving_angle = frame * 0.01
        for i, (gear, line) in enumerate(zip(self.gears, self.lines)):
            angle = driving_angle / (self.gear_ratio**i) * (-1 if i % 2 == 1 else 1)
            rotation_matrix = np.array([
                [np.cos(angle), -np.sin(angle)],
                [np.sin(angle), np.cos(angle)]
            ])
            rotated_gear = (gear - self.positions[i]) @ rotation_matrix.T + self.positions[i]
            line.set_data(rotated_gear[:, 0], rotated_gear[:, 1])
        return self.lines

    def run(self):
        """Run the simulation and save the animation as a GIF."""
        anim = FuncAnimation(self.fig, self.update, frames=360, interval=20, blit=True)
        anim.save("gear_reduction_simulation.gif", writer=PillowWriter(fps=30))
        return "gear_reduction_simulation.gif"

if __name__ == "__main__":
    st.title("Gear Reduction Simulation")
    sim = GearReductionSimulation(n_gears=20, initial_radius=10, gear_ratio=2, spacing=12)
    gif_path = sim.run()
    st.image(gif_path)
