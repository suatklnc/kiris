import numpy as np
from rich.panel import Panel


class ASCIIPlotter:

    """
    Utility to create ASCII diagrams for SFD and BMD.
    """

    def __init__(self, width: int = 60, height: int = 15):
        self.width = width
        self.height = height

    def plot(self, x_points: np.ndarray, y_points: np.ndarray, title: str) -> Panel:
        """
        Creates an ASCII plot within a Rich Panel.
        """
        # Normalize points to grid
        grid = [[" " for _ in range(self.width)] for _ in range(self.height)]

        y_min, y_max = min(y_points), max(y_points)
        if y_min == y_max:
            y_min, y_max = y_min - 1, y_max + 1

        x_min, x_max = min(x_points), max(x_points)

        # Zero line index
        zero_y_idx = int((0 - y_min) / (y_max - y_min) * (self.height - 1))
        zero_y_idx = max(0, min(self.height - 1, zero_y_idx))
        # Flip Y for grid (0 is top)
        zero_grid_y = (self.height - 1) - zero_y_idx

        # Draw zero line
        for x in range(self.width):
            grid[zero_grid_y][x] = "─"

        # Plot points
        for i in range(len(x_points)):
            grid_x = int((x_points[i] - x_min) / (x_max - x_min) * (self.width - 1))
            grid_y_idx = int(
                (y_points[i] - y_min) / (y_max - y_min) * (self.height - 1)
            )
            grid_y = (self.height - 1) - grid_y_idx

            # Use color-coded characters
            if y_points[i] > 0.001:
                grid[grid_y][grid_x] = "[green]█[/green]"
            elif y_points[i] < -0.001:
                grid[grid_y][grid_x] = "[red]█[/red]"
            else:
                grid[grid_y][grid_x] = "█"

        plot_str = "\n".join(["".join(row) for row in grid])
        return Panel(
            plot_str, title=title, subtitle=f"Min: {y_min:.2f} | Max: {y_max:.2f}"
        )
