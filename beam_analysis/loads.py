from abc import ABC
from dataclasses import dataclass


@dataclass
class Load(ABC):
    """Base class for all loads."""

    pass


@dataclass
class PointLoad(Load):
    """
    A point load applied at a specific location on the beam.

    Attributes:
        force (float): The magnitude of the force in kN. Positive is downwards.
        location (float): The location of the load in meters from the left support.
    """

    force: float
    location: float

    def __post_init__(self):
        if self.location < 0:
            raise ValueError("Location cannot be negative.")

    def __str__(self):
        return f"PointLoad(force={self.force} kN, location={self.location} m)"


@dataclass
class UDL(Load):
    """
    A uniformly distributed load applied over the entire beam span.

    Attributes:
        magnitude (float): The magnitude of the load in kN/m. Positive is downwards.
    """

    magnitude: float

    def __str__(self):
        return f"UDL(magnitude={self.magnitude} kN/m)"
