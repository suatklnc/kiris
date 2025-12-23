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
                # UDL is over the entire beam length
                total_load = load.magnitude * self.beam.length
                # Centroid of full-span UDL is at length/2
                centroid = self.beam.length / 2.0
                total_moment_x1 += total_load * (centroid - x1)
                total_vertical_force += total_load
        
        r2 = -total_moment_x1 / l_span
        r1 = -total_vertical_force - r2
        
        return {x1: r1, x2: r2}
