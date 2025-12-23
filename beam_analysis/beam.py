from dataclasses import dataclass
from typing import Tuple

@dataclass
class Beam:
    """
    Represents a beam with a specific length and supports.

    Attributes:
        length (float): The total length of the beam in meters.
        supports (Tuple[float, ...]): The locations of the supports in meters.
    """
    length: float
    supports: Tuple[float, ...]

    def __post_init__(self):
        if self.length <= 0:
            raise ValueError("Length must be positive.")
        
        for support in self.supports:
            if support < 0 or support > self.length:
                raise ValueError(f"Support location must be within beam limits (0 to {self.length}).")

    def __str__(self):
        return f"Beam(length={self.length} m, supports={self.supports})"
