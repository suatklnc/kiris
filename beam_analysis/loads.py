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
    A uniformly distributed load applied over a span of the beam.

    Attributes:
        magnitude (float): The magnitude of the load in kN/m. Positive is downwards.
        start (float): The start location of the load in meters. Defaults to 0.0.
        end (float | None): The end location of the load in meters. 
                            If None, it extends to the end of the beam.
    """

    magnitude: float
    start: float = 0.0
    end: float | None = None

    def __post_init__(self):
        if self.start < 0:
            raise ValueError("Start location cannot be negative.")
        if self.end is not None and self.end < 0:
            raise ValueError("End location cannot be negative.")
        if self.end is not None and self.start >= self.end:
            raise ValueError("Start location must be less than end location.")

    def __str__(self):
        end_str = f"{self.end} m" if self.end is not None else "End"
        return f"UDL(magnitude={self.magnitude} kN/m, start={self.start} m, end={end_str})"


@dataclass
class PointMoment(Load):
    """
    A concentrated moment applied at a specific location on the beam.

    Attributes:
        moment (float): The magnitude of the moment in kNm. Positive is clockwise.
        location (float): The location of the moment in meters from the left support.
    """

    moment: float
    location: float

    def __post_init__(self):
        if self.location < 0:
            raise ValueError("Location cannot be negative.")

    def __str__(self):
        return f"PointMoment(moment={self.moment} kNm, location={self.location} m)"
