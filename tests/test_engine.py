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
