import numpy as np
from typing import List, Dict, Tuple
from beam_analysis.beam import Beam
from beam_analysis.loads import Load, PointLoad, UDL, PointMoment


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

    def calculate_reactions(self) -> Dict[float, Dict[str, float]]:
        """
        Calculates the reaction forces and moments at the supports.
        
        Returns:
            Dict[float, Dict[str, float]]: A dictionary mapping support location 
                                           to a dict of reactions {'fy': force, 'm': moment}.
        """
        from beam_analysis.beam import SupportType
        
        if len(self.beam.supports) == 1:
            support = self.beam.supports[0]
            if support.type != SupportType.FIXED:
                raise ValueError("Single support must be FIXED.")
            
            total_vertical_force = 0.0
            total_moment_at_support = 0.0
            
            for load in self.loads:
                if isinstance(load, PointLoad):
                    total_vertical_force += load.force
                    total_moment_at_support += load.force * (load.location - support.location)
                elif isinstance(load, UDL):
                    start = load.start
                    end = load.end if load.end is not None else self.beam.length
                    end = min(end, self.beam.length)
                    span_len = end - start
                    if span_len > 0:
                        total_load = load.magnitude * span_len
                        centroid = start + (span_len / 2.0)
                        total_vertical_force += total_load
                        total_moment_at_support += total_load * (centroid - support.location)
                elif isinstance(load, PointMoment):
                    total_moment_at_support += load.moment
            
            # Reaction moment is opposite to the applied moment
            return {support.location: {'fy': total_vertical_force, 'm': -total_moment_at_support}}

        if len(self.beam.supports) != 2:
            raise NotImplementedError(
                "Currently only 1 fixed support or 2 pinned/roller supports are supported."
            )

        s1, s2 = sorted(self.beam.supports, key=lambda s: s.location)
        x1, x2 = s1.location, s2.location
        l_span = x2 - x1

        total_moment_x1 = 0.0
        total_vertical_force = 0.0

        for load in self.loads:
            if isinstance(load, PointLoad):
                total_moment_x1 += load.force * (load.location - x1)
                total_vertical_force += load.force
            elif isinstance(load, UDL):
                start = load.start
                end = load.end if load.end is not None else self.beam.length
                end = min(end, self.beam.length)
                
                span_len = end - start
                if span_len > 0:
                    total_load = load.magnitude * span_len
                    centroid = start + (span_len / 2.0)
                    total_moment_x1 += total_load * (centroid - x1)
                    total_vertical_force += total_load
            elif isinstance(load, PointMoment):
                total_moment_x1 += load.moment

        r2 = total_moment_x1 / l_span
        r1 = total_vertical_force - r2

        return {
            x1: {'fy': r1, 'm': 0.0},
            x2: {'fy': r2, 'm': 0.0}
        }

    def get_shear_force(self, x: float) -> float:
        """
        Calculates the shear force at position x from the left end of the beam.

        Args:
            x (float): Position along the beam (0 to length).

        Returns:
            float: Shear force in kN.
        """
        if x < 0 or x > self.beam.length:
            raise ValueError(
                f"Position x={x} is outside the beam limits (0 to {self.beam.length})."
            )

        reactions = self.calculate_reactions()
        v = 0.0

        # Add reactions to the left of x
        for support_loc, rx in reactions.items():
            if support_loc <= x:
                v += rx['fy']

        # Add loads to the left of x
        for load in self.loads:
            if isinstance(load, PointLoad):
                if load.location <= x:
                    v -= load.force
            elif isinstance(load, UDL):
                start = load.start
                end = load.end if load.end is not None else self.beam.length
                
                if x > start:
                    effective_end = min(x, end)
                    span = effective_end - start
                    if span > 0:
                        v -= load.magnitude * span

        return v

    def get_bending_moment(self, x: float) -> float:
        """
        Calculates the bending moment at position x from the left end of the beam.

        Args:
            x (float): Position along the beam (0 to length).

        Returns:
            float: Bending moment in kNm.
        """
        if x < 0 or x > self.beam.length:
            raise ValueError(
                f"Position x={x} is outside the beam limits (0 to {self.beam.length})."
            )

        reactions = self.calculate_reactions()
        m = 0.0

        # Moment from reactions to the left of x
        for support_loc, rx in reactions.items():
            if support_loc <= x:
                m += rx['fy'] * (x - support_loc)
                m += rx['m']  # Include reaction moment (like fixed support)

        # Moment from loads to the left of x
        for load in self.loads:
            if isinstance(load, PointLoad):
                if load.location <= x:
                    m -= load.force * (x - load.location)
            elif isinstance(load, UDL):
                start = load.start
                end = load.end if load.end is not None else self.beam.length
                
                if x > start:
                    effective_end = min(x, end)
                    span = effective_end - start
                    if span > 0:
                        load_portion = load.magnitude * span
                        centroid = start + (span / 2.0)
                        m -= load_portion * (x - centroid)
            elif isinstance(load, PointMoment):
                if load.location <= x:
                    m += load.moment

        return m

    def get_max_shear_info(self) -> Tuple[float, float]:
        """
        Finds the maximum shear force and its location.

        Returns:
            Tuple[float, float]: (max_shear_value, location_x)
        """
        x_points = np.linspace(0, self.beam.length, 1000)
        v_points = [self.get_shear_force(x) for x in x_points]

        # For point loads, we should also check just before the load location
        for load in self.loads:
            if isinstance(load, PointLoad):
                if load.location > 0.001:
                    v_points.append(self.get_shear_force(load.location - 0.001))
                v_points.append(self.get_shear_force(load.location))

        v_abs = [abs(v) for v in v_points]
        max_idx = np.argmax(v_abs)
        # Simplified: if multiple max, we just take one.
        # This is a bit rough for location, but good enough for MVP.
        return v_points[max_idx], x_points[min(max_idx, len(x_points) - 1)]

    def get_max_moment_info(self) -> Tuple[float, float]:
        """
        Finds the maximum bending moment and its location.

        Returns:
            Tuple[float, float]: (max_moment_value, location_x)
        """
        x_points = np.linspace(0, self.beam.length, 1000)
        # Also include load locations and support locations for exact results
        critical_points = set(x_points)
        critical_points.update([s.location for s in self.beam.supports])
        # Add middle of the beam as it's critical for UDL (legacy)
        critical_points.add(self.beam.length / 2.0)
        for load in self.loads:
            if isinstance(load, PointLoad):
                critical_points.add(load.location)
            elif isinstance(load, PointMoment):
                critical_points.add(load.location)
                if load.location > 0.001:
                    critical_points.add(load.location - 0.001)
            elif isinstance(load, UDL):
                critical_points.add(load.start)
                end = load.end if load.end is not None else self.beam.length
                critical_points.add(end)

        sorted_points = sorted(list(critical_points))
        m_points = [self.get_bending_moment(x) for x in sorted_points]

        m_abs = [abs(m) for m in m_points]
        max_idx = np.argmax(m_abs)
        return m_points[max_idx], sorted_points[max_idx]
