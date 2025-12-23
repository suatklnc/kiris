import pytest
from beam_analysis.beam import Beam, Support, SupportType
from beam_analysis.engine import AnalysisEngine
from beam_analysis.loads import PointLoad, UDL


def test_cantilever_point_load():
    # 5m beam, fixed at 0.0
    beam = Beam(length=5.0, supports=[Support(0.0, SupportType.FIXED)])
    engine = AnalysisEngine(beam=beam)
    
    # 10kN load at 5m (free end)
    engine.add_load(PointLoad(force=10.0, location=5.0))
    
    reactions = engine.calculate_reactions()
    # Ra = 10kN
    assert reactions[0.0]['fy'] == pytest.approx(10.0)
    # Ma = 10 * 5 = 50kNm (Reaction moment should be -50 to balance applied 50)
    assert reactions[0.0]['m'] == pytest.approx(-50.0)
    
    # Shear at x=2.5 should be 10kN
    assert engine.get_shear_force(2.5) == pytest.approx(10.0)
    
    # Moment at x=0
    assert engine.get_bending_moment(0.0) == pytest.approx(-50.0)
    
    # Moment at x=5 should be 0
    assert engine.get_bending_moment(5.0) == pytest.approx(0.0)

def test_cantilever_udl():
    # 4m beam, fixed at 0.0
    beam = Beam(length=4.0, supports=[Support(0.0, SupportType.FIXED)])
    engine = AnalysisEngine(beam=beam)
    
    # 2kN/m UDL over full span
    engine.add_load(UDL(magnitude=2.0))
    
    reactions = engine.calculate_reactions()
    # Ra = 2 * 4 = 8kN
    assert reactions[0.0]['fy'] == pytest.approx(8.0)
    # Ma = -(8 * 2) = -16kNm
    assert reactions[0.0]['m'] == pytest.approx(-16.0)
    
    # Moment at x=0: -16kNm
    assert engine.get_bending_moment(0.0) == pytest.approx(-16.0)
    
    # Shear at x=0: 8kN
    assert engine.get_shear_force(0.0) == pytest.approx(8.0)
    # Shear at x=4: 0
    assert engine.get_shear_force(3.999) == pytest.approx(0.0, abs=1e-2)
