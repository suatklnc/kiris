from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum, auto


class SupportType(Enum):
    PINNED = auto()  # Sabit mesnet (Restrains x, y)
    ROLLER = auto()  # Hareketli mesnet (Restrains y)
    FIXED = auto()   # Ankastre mesnet (Restrains x, y, rotation)


@dataclass
class Support:
    location: float
    type: SupportType = SupportType.ROLLER

    def __str__(self):
        return f"{self.type.name} at {self.location}m"


@dataclass
class Beam:
    """
    Represents a beam with a specific length and supports.

    Attributes:
        length (float): The total length of the beam in meters.
        supports (List[Support]): The list of supports on the beam.
    """

    length: float
    supports: List[Support]

    def __post_init__(self):
        if self.length <= 0:
            raise ValueError("Length must be positive.")

        for support in self.supports:
            if support.location < 0 or support.location > self.length:
                raise ValueError(
                    f"Support location must be within beam limits (0 to {self.length})."
                )

    def __str__(self):
        supports_str = ", ".join([str(s) for s in self.supports])
        return f"Beam(length={self.length} m, supports=[{supports_str}])"
