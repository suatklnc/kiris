from beam_analysis.beam import Beam
from beam_analysis.loads import PointLoad
from beam_analysis.engine import AnalysisEngine
from beam_analysis.cli import display_results
from rich.console import Console

def test_display_results_smoke():
    # Smoke test to ensure display_results doesn't crash
    beam = Beam(length=10.0, supports=(0.0, 10.0))
    engine = AnalysisEngine(beam=beam)
    engine.add_load(PointLoad(force=-10.0, location=5.0))
    
    # We just call it to see if it runs without error
    # Real output verification is hard for Rich console
    display_results(engine)
