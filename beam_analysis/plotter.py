import numpy as np
from rich.panel import Panel
from rich.table import Table
from rich.console import Group
from beam_analysis.beam import Beam, SupportType
from beam_analysis.loads import PointLoad, UDL, PointMoment


class ASCIIPlotter:

    """
    Utility to create ASCII diagrams for SFD and BMD.
    """

    def __init__(self, width: int = 60, height: int = 15):
        self.width = width
        self.height = height

    def plot_beam_schematic(self, beam: Beam, loads: list) -> Panel:
        """
        Creates a schematic representation of the beam, supports, and loads.
        """
        grid_height = 5
        grid = [[" " for _ in range(self.width)] for _ in range(grid_height)]
        beam_y = 2  # Middle row for beam line

        # Draw beam line
        for x in range(self.width):
            grid[beam_y][x] = "═"

        # Helper to scale x to grid x
        def get_grid_x(location: float):
            val = int((location / beam.length) * (self.width - 1))
            return max(0, min(self.width - 1, val))

        # Draw Supports
        for support in beam.supports:
            gx = get_grid_x(support.location)
            if support.type == SupportType.PINNED:
                grid[beam_y + 1][gx] = "▲"  # Support point
                grid[beam_y + 2][gx] = "┴"  # Base
            elif support.type == SupportType.ROLLER:
                grid[beam_y + 1][gx] = "○"  # Roller
                grid[beam_y + 2][gx] = "─"  # Ground
            elif support.type == SupportType.FIXED:
                # Vertical wall
                if support.location == 0:
                    grid[beam_y - 1][gx] = "│"
                    grid[beam_y][gx] = "├"
                    grid[beam_y + 1][gx] = "│"
                elif support.location == beam.length:
                    grid[beam_y - 1][gx] = "│"
                    grid[beam_y][gx] = "┤"
                    grid[beam_y + 1][gx] = "│"
                else:
                    # Fixed inside (less common, show as clamped block)
                    grid[beam_y][gx] = "█"
                    grid[beam_y + 1][gx] = "┴"

        # Draw Loads (Simplified)
        for load in loads:
            if isinstance(load, PointLoad):
                gx = get_grid_x(load.location)
                if load.force > 0: # Downward
                    grid[beam_y - 1][gx] = "↓"
                else: # Upward
                    grid[beam_y + 1][gx] = "↑"
            elif isinstance(load, PointMoment):
                gx = get_grid_x(load.location)
                grid[beam_y - 1][gx] = "↻" if load.moment > 0 else "↺"
            elif isinstance(load, UDL):
                start_gx = get_grid_x(load.start)
                end = load.end if load.end is not None else beam.length
                end_gx = get_grid_x(end)
                for x in range(start_gx, end_gx + 1):
                    grid[beam_y - 1][x] = "w"

        plot_str = "\n".join(["".join(row) for row in grid])
        legend = "\n[bold]Legend:[/bold] ▲=Pinned, ○=Roller, │=Fixed, ↓=Point Load, w=UDL, ↻=Moment"
        return Panel(plot_str + legend, title="Kiriş Şeması (Beam Schematic)", expand=False)

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
