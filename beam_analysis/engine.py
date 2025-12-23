from typing import List, Dict
from beam_analysis.beam import Beam
from beam_analysis.loads import Load, PointLoad, UDL

class AnalysisEngine:
    """
    The core calculation engine for beam analysis.
    
    Attributes:
        beam (Beam): The beam to be analyzed.
        loads (List[Load]): A list of loads applied to the beam.
    """
    def __init__(self, beam: Beam):
        self.beam = beam
        self.loads: List[Load] = []

    def add_load(self, load: Load):
        """Adds a load to the beam for analysis."""
        self.loads.append(load)

    def calculate_reactions(self) -> Dict[float, float]:
        """
        Calculates the reaction forces at the supports.
        Only supports two supports (statically determinate beam) for now.
        
        Returns:
            Dict[float, float]: A dictionary mapping support location to reaction force.
        """
        if len(self.beam.supports) != 2:
            raise NotImplementedError("Only beams with exactly 2 supports are supported.")
        
        x1, x2 = self.beam.supports
        l_span = x2 - x1
        
        total_moment_x1 = 0.0
        total_vertical_force = 0.0

        for load in self.loads:
            if isinstance(load, PointLoad):
                total_moment_x1 += load.force * (load.location - x1)
                total_vertical_force += load.force
            elif isinstance(load, UDL):
                total_load = load.magnitude * self.beam.length
                centroid = self.beam.length / 2.0
                total_moment_x1 += total_load * (centroid - x1)
                total_vertical_force += total_load
        
        r2 = -total_moment_x1 / l_span
        r1 = -total_vertical_force - r2
        
        return {x1: r1, x2: r2}

    def get_shear_force(self, x: float) -> float:
        """
        Calculates the shear force at position x from the left end of the beam.
        
        Args:
            x (float): Position along the beam (0 to length).
            
        Returns:
            float: Shear force in kN.
        """
        if x < 0 or x > self.beam.length:
            raise ValueError(f"Position x={x} is outside the beam limits (0 to {self.beam.length}).")

        reactions = self.calculate_reactions()
        v = 0.0
        
        # Add reactions to the left of x
        for support_loc, force in reactions.items():
            if support_loc <= x:
                v += force
                
        # Add loads to the left of x
        for load in self.loads:
            if isinstance(load, PointLoad):
                if load.location <= x:
                    v += load.force
            elif isinstance(load, UDL):
                # UDL is over the entire span, so we take the portion from 0 to x
                v += load.magnitude * x
                
        return v
