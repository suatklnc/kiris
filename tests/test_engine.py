import pytest
from beam_analysis.beam import Beam
from beam_analysis.engine import AnalysisEngine

def test_engine_initialization():
    beam = Beam(length=10.0, supports=(0.0, 10.0))
    engine = AnalysisEngine(beam=beam)
    assert engine.beam == beam
    assert engine.loads == []

def test_engine_add_load():
    from beam_analysis.loads import PointLoad
    beam = Beam(length=10.0, supports=(0.0, 10.0))
    engine = AnalysisEngine(beam=beam)
    load = PointLoad(force=-10.0, location=5.0)
    engine.add_load(load)
    assert len(engine.loads) == 1
    assert engine.loads[0] == load

def test_calculate_reactions_point_load_center():
    from beam_analysis.loads import PointLoad
    # 10m beam, supports at 0 and 10
    beam = Beam(length=10.0, supports=(0.0, 10.0))
    engine = AnalysisEngine(beam=beam)
    # 10kN downward load at 5m
    load = PointLoad(force=-10.0, location=5.0)
    engine.add_load(load)
    reactions = engine.calculate_reactions()
    # Expect 5kN upward at each support
    assert reactions[0] == pytest.approx(5.0)
    assert reactions[10.0] == pytest.approx(5.0)

def test_calculate_reactions_point_load_off_center():
    from beam_analysis.loads import PointLoad
    beam = Beam(length=10.0, supports=(0.0, 10.0))
    engine = AnalysisEngine(beam=beam)
    # 10kN downward load at 2.5m (1/4 of the way)
    load = PointLoad(force=-10.0, location=2.5)
    engine.add_load(load)
    reactions = engine.calculate_reactions()
    # Ra (at 0) should be 7.5kN, Rb (at 10) should be 2.5kN
    assert reactions[0.0] == pytest.approx(7.5)
    assert reactions[10.0] == pytest.approx(2.5)

def test_calculate_reactions_udl_full_span():
    from beam_analysis.loads import UDL
    beam = Beam(length=10.0, supports=(0.0, 10.0))
    engine = AnalysisEngine(beam=beam)
    # 5kN/m downward UDL over 10m
    load = UDL(magnitude=-5.0)
    engine.add_load(load)
    reactions = engine.calculate_reactions()
    # Total load is 50kN, Ra and Rb should be 25kN each
    assert reactions[0.0] == pytest.approx(25.0)
    assert reactions[10.0] == pytest.approx(25.0)

def test_calculate_reactions_combined_loads():
    from beam_analysis.loads import PointLoad, UDL
    beam = Beam(length=10.0, supports=(0.0, 10.0))
    engine = AnalysisEngine(beam=beam)
    # 10kN downward point load at 5m
    engine.add_load(PointLoad(force=-10.0, location=5.0))
    # 5kN/m downward UDL over 10m
    engine.add_load(UDL(magnitude=-5.0))
    reactions = engine.calculate_reactions()
    # Ra and Rb should be (10 + 50) / 2 = 30kN each
    assert reactions[0.0] == pytest.approx(30.0)
    assert reactions[10.0] == pytest.approx(30.0)
