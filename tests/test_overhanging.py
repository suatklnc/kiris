import pytest
from beam_analysis.beam import Beam, Support, SupportType
from beam_analysis.engine import AnalysisEngine
from beam_analysis.loads import PointLoad, UDL

def test_overhanging_beam_point_load():
    """
    Test a beam with supports not at the ends (Overhanging Beam).
    Beam Length: 10m
    Supports at: 2m and 8m (Span = 6m)
    Load: 10kN at 5m (Mid-span between supports)
    """
    # Supports at 2.0m and 8.0m
    supports = [Support(2.0, SupportType.PINNED), Support(8.0, SupportType.ROLLER)]
    beam = Beam(length=10.0, supports=supports)
    engine = AnalysisEngine(beam=beam)
    
    # Load at 5.0m (center of the 2-8 span)
    engine.add_load(PointLoad(force=10.0, location=5.0))
    
    reactions = engine.calculate_reactions()
    
    # Due to symmetry, each support takes half the load
    # Ra (at 2m) = 5kN, Rb (at 8m) = 5kN
    assert reactions[2.0]['fy'] == pytest.approx(5.0)
    assert reactions[8.0]['fy'] == pytest.approx(5.0)
    
    # Shear force checks
    # x=1.0 (Left overhang): V = 0
    assert engine.get_shear_force(1.0) == pytest.approx(0.0)
    # x=3.0 (Between Ra and Load): V = Ra = 5
    assert engine.get_shear_force(3.0) == pytest.approx(5.0)
    # x=6.0 (Between Load and Rb): V = Ra - 10 = -5
    assert engine.get_shear_force(6.0) == pytest.approx(-5.0)
    # x=9.0 (Right overhang): V = Ra - 10 + Rb = 5 - 10 + 5 = 0
    assert engine.get_shear_force(9.0) == pytest.approx(0.0)

def test_overhanging_beam_udl_on_overhang():
    """
    Test load on the overhang part.
    Beam Length: 10m
    Supports at: 2m and 10m
    Load: 10kN point load at 0m (Tip of left overhang)
    """
    supports = [Support(2.0, SupportType.PINNED), Support(10.0, SupportType.ROLLER)]
    beam = Beam(length=10.0, supports=supports)
    engine = AnalysisEngine(beam=beam)
    
    # Load at 0.0m
    engine.add_load(PointLoad(force=10.0, location=0.0))
    
    reactions = engine.calculate_reactions()
    
    # Take moment about support B (10m):
    # Load * (10 - 0) - Ra * (10 - 2) = 0
    # 10 * 10 - Ra * 8 = 0 -> 8Ra = 100 -> Ra = 12.5 kN (Upward)
    # Fy = 0 -> Ra + Rb - 10 = 0 -> Rb = 10 - 12.5 = -2.5 kN (Downward)
    
    assert reactions[2.0]['fy'] == pytest.approx(12.5)
    assert reactions[10.0]['fy'] == pytest.approx(-2.5)
    
    # Shear at x=1.0: V = -10 (Load is downward)
    assert engine.get_shear_force(1.0) == pytest.approx(-10.0)
    
    # Shear at x=3.0: V = -10 + 12.5 = 2.5
    assert engine.get_shear_force(3.0) == pytest.approx(2.5)
    
    # Moment at support A (x=2.0):
    # From left: -10 * (2 - 0) = -20 kNm
    assert engine.get_bending_moment(2.0) == pytest.approx(-20.0)
