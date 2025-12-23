from typing import List
from beam_analysis.beam import Beam
from beam_analysis.loads import Load

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
