import numpy as np
from typing import Dict, List, Tuple
from beam_analysis.beam import Beam, SupportType
from beam_analysis.loads import Load, PointLoad, UDL, PointMoment

class MatrixBeamSolver:
    """
    A Finite Element Method (FEM) based solver for 1D beam analysis using the 
    Direct Stiffness Method. This allows solving statically indeterminate beams.
    """

    def __init__(self, beam: Beam, loads: List[Load]):
        self.beam = beam
        self.loads = loads
        self.nodes = self._generate_nodes()
        self.EI = 1.0e6  # Arbitrary value for uniform beam reaction calculation
        
        # Degrees of Freedom: 2 per node (Vertical Translation v, Rotation theta)
        self.n_dof = len(self.nodes) * 2

    def _generate_nodes(self) -> List[float]:
        """Generates sorted unique node locations based on beam features."""
        points = {0.0, self.beam.length}
        
        for support in self.beam.supports:
            points.add(support.location)
            
        for load in self.loads:
            if isinstance(load, PointLoad):
                points.add(load.location)
            elif isinstance(load, PointMoment):
                points.add(load.location)
            elif isinstance(load, UDL):
                points.add(load.start)
                end = load.end if load.end is not None else self.beam.length
                points.add(end)
        
        return sorted(list(points))

    def solve_reactions(self) -> Dict[float, Dict[str, float]]:
        """
        Solves the system and returns reactions at supported nodes.
        Returns format compatible with AnalysisEngine: {location: {'fy': val, 'm': val}}
        """
        K = np.zeros((self.n_dof, self.n_dof))
        F = np.zeros(self.n_dof)
        
        # 1. Assemble Global Stiffness Matrix and Equivalent Nodal Loads
        for i in range(len(self.nodes) - 1):
            x1 = self.nodes[i]
            x2 = self.nodes[i+1]
            L = x2 - x1
            
            if L <= 1e-9:
                continue
                
            # Element Stiffness Matrix
            # Coordinate system: Y positive UP, Moment positive CCW
            # DOFs: [v1, theta1, v2, theta2]
            k_local = (self.EI / L**3) * np.array([
                [12,      6*L,    -12,     6*L],
                [6*L,     4*L**2, -6*L,    2*L**2],
                [-12,     -6*L,    12,     -6*L],
                [6*L,     2*L**2, -6*L,    4*L**2]
            ])
            
            # Map to global indices
            indices = [2*i, 2*i+1, 2*(i+1), 2*(i+1)+1]
            for r in range(4):
                for c in range(4):
                    K[indices[r], indices[c]] += k_local[r, c]
            
            # Equivalent Nodal Loads from UDL
            # Check for UDLs on this element
            w_segment = 0.0 # Net distributed load (Positive UP)
            
            mid_point = (x1 + x2) / 2.0
            for load in self.loads:
                if isinstance(load, UDL):
                    end = load.end if load.end is not None else self.beam.length
                    # Handle floating point precision with epsilon
                    if load.start <= mid_point and end >= mid_point:
                        # User UDL is positive DOWN. My system Y is UP.
                        w_segment += (-load.magnitude)
            
            if abs(w_segment) > 1e-9:
                # Fixed End Actions for Uniform Load w (Positive UP)
                # Left (Node 1): Fy = wL/2, M = wL^2/12
                # Right (Node 2): Fy = wL/2, M = -wL^2/12
                fem_v1 = w_segment * L / 2
                fem_m1 = w_segment * L**2 / 12
                fem_v2 = w_segment * L / 2
                fem_m2 = -w_segment * L**2 / 12
                
                # Add Equivalent Nodal Loads (Negative of FEM) to F
                F[2*i]     += fem_v1
                F[2*i+1]   += fem_m1
                F[2*(i+1)] += fem_v2
                F[2*(i+1)+1] += fem_m2

        # 2. Add Nodal Loads (Point Loads / Moments)
        for load in self.loads:
            if isinstance(load, (PointLoad, PointMoment)):
                # Find closest node index
                # (Using min distance to handle float precision)
                idx = np.argmin(np.abs(np.array(self.nodes) - load.location))
                
                if isinstance(load, PointLoad):
                    # User Force positive DOWN -> My Y positive UP -> Add -Force
                    F[2*idx] += (-load.force)
                elif isinstance(load, PointMoment):
                    # User Moment positive CW -> My Moment positive CCW -> Add -Moment
                    F[2*idx+1] += (-load.moment)

        # 3. Apply Boundary Conditions
        constrained_dofs = []
        
        # We need to map support location to node index
        support_indices = {}
        for support in self.beam.supports:
            idx = np.argmin(np.abs(np.array(self.nodes) - support.location))
            support_indices[idx] = support
            
            # Apply constraints
            # v (vertical) is always constrained for all support types
            constrained_dofs.append(2*idx) 
            
            if support.type == SupportType.FIXED:
                # theta (rotation) is also constrained
                constrained_dofs.append(2*idx+1)

        constrained_dofs = sorted(list(set(constrained_dofs)))
        free_dofs = [i for i in range(self.n_dof) if i not in constrained_dofs]
        
        # 4. Solve for Displacements
        # Partition matrices
        K_ff = K[np.ix_(free_dofs, free_dofs)]
        F_f = F[free_dofs]
        
        # Solve K_ff * d_f = F_f
        d_f = np.linalg.solve(K_ff, F_f)
        
        # Construct full displacement vector
        d_global = np.zeros(self.n_dof)
        d_global[free_dofs] = d_f
        # d_global[constrained_dofs] is 0.0 (homogeneous BCs)
        
        # 5. Calculate Reactions
        # R = K * d - F_external
        # Note: F vector currently contains Equivalent Nodal Loads + Point Loads.
        # We want the reaction force which balances the internal force and external load.
        # Equilibrium at node: R + F_external = F_internal (K*d)
        # So R = K*d - F_external
        # However, F constructed above *is* the external load vector (including equivalent nodal loads).
        # So R = K * d_global - F
        
        internal_forces = K @ d_global
        reactions_vector = internal_forces - F
        
        results = {}
        for idx, support in support_indices.items():
            # Extract reaction from vector
            r_y = reactions_vector[2*idx]
            r_m = reactions_vector[2*idx+1]
            
            # Convert back to user sign convention
            # My Y UP -> User Y UP (Wait, user convention:
            # In engine.py: return {'fy': force, 'm': moment}
            # Standard: Reaction UP is positive.
            # My calc: r_y is UP (because Y is UP).
            
            # User Moment:
            # In engine.py: "Reaction moment is opposite to the applied moment"
            # It seems user expects reaction moment convention. 
            # If I have a fixed support and I apply CW moment, reaction is CCW.
            # My calc: r_m is CCW.
            # Let's check engine.py for single fixed support:
            # load.force (Down) -> total_vertical_force += load.force (Down sum)
            # return fy: total_vertical_force. 
            # WAIT. If load is Down, reaction must be Up.
            # If engine.py returns positive for Upward reaction resisting Downward load:
            # load.force (positive) is DOWN.
            # reaction should be UP.
            # engine.py: total_vertical_force += load.force -> returns this.
            # So engine output Positive = UP (magnitude equal to load).
            # My r_y is Positive UP. So `fy` = r_y.
            
            # For Moment:
            # load.moment (CW).
            # total_moment += load.moment.
            # returns 'm': -total_moment.
            # So if load is CW (Pos), reaction is -Pos = Neg.
            # Neg = CCW.
            # My r_m is CCW.
            # So if r_m is positive (CCW), it matches the sign of -total_moment (CCW).
            # So `m` = r_m.
            
            results[support.location] = {
                'fy': r_y,
                'm': r_m
            }
            
        return results
