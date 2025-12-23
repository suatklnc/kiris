import pytest
from beam_analysis.beam import Beam, Support, SupportType
from beam_analysis.loads import UDL, PointLoad
from beam_analysis.engine import AnalysisEngine

def test_three_support_beam_udl():
    """
    Test a continuous beam with 3 supports (Indeterminate).
    Span 1: 4m, Span 2: 6m.
    Load: UDL 10 kN/m on Span 2.
    """
    # Create Beam
    beam = Beam(
        length=10.0,
        supports=[
            Support(0.0, SupportType.PINNED),
            Support(4.0, SupportType.PINNED),
            Support(10.0, SupportType.ROLLER),
        ]
    )
    
    # Create Engine
    engine = AnalysisEngine(beam)
    
    # Add Load: 10 kN/m from 4.0 to 10.0
    engine.add_load(UDL(magnitude=10.0, start=4.0, end=10.0))
    
    # Calculate Reactions
    reactions = engine.calculate_reactions()
    
    # Expected values (Calculated manually via Three-Moment Equation)
    # R1 (x=0) = -6.75 kN
    # R2 (x=4) = 41.25 kN
    # R3 (x=10) = 25.5 kN
    
    r1 = reactions[0.0]['fy']
    r2 = reactions[4.0]['fy']
    r3 = reactions[10.0]['fy']
    
    print(f"Reactions: R1={r1}, R2={r2}, R3={r3}")
    
    assert r1 == pytest.approx(-6.75, abs=0.01)
    assert r2 == pytest.approx(41.25, abs=0.01)
    assert r3 == pytest.approx(25.5, abs=0.01)

def test_four_support_uniform_load():
    """
    Test a continuous beam with 4 supports (3 equal spans of 10m).
    Total length 30m.
    UDL 12 kN/m over entire length.
    Coefficients for reactions on equal span continuous beam:
    Outer supports: 0.4 wL
    Inner supports: 1.1 wL
    L = 10, w = 12.
    Outer: 0.4 * 12 * 10 = 48 kN
    Inner: 1.1 * 12 * 10 = 132 kN
    Total load = 12 * 30 = 360.
    Total reactions = 48*2 + 132*2 = 96 + 264 = 360.
    """
    beam = Beam(
        length=30.0,
        supports=[
            Support(0.0, SupportType.PINNED),
            Support(10.0, SupportType.ROLLER),
            Support(20.0, SupportType.ROLLER),
            Support(30.0, SupportType.ROLLER),
        ]
    )
    
    engine = AnalysisEngine(beam)
    engine.add_load(UDL(magnitude=12.0, start=0.0, end=30.0))
    
    reactions = engine.calculate_reactions()
    
    r_outer_1 = reactions[0.0]['fy']
    r_inner_1 = reactions[10.0]['fy']
    r_inner_2 = reactions[20.0]['fy']
    r_outer_2 = reactions[30.0]['fy']
    
    assert r_outer_1 == pytest.approx(48.0, abs=0.1)
    assert r_outer_2 == pytest.approx(48.0, abs=0.1)
    assert r_inner_1 == pytest.approx(132.0, abs=0.1)
    assert r_inner_2 == pytest.approx(132.0, abs=0.1)
