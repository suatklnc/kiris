import pytest
from beam_analysis.beam import Beam

def test_beam_initialization():
    beam = Beam(length=10.0, supports=(0.0, 10.0))
    assert beam.length == 10.0
    assert beam.supports == (0.0, 10.0)

def test_beam_invalid_length():
    with pytest.raises(ValueError, match="Length must be positive"):
        Beam(length=-5.0, supports=(0.0, 5.0))

def test_beam_zero_length():
    with pytest.raises(ValueError, match="Length must be positive"):
        Beam(length=0.0, supports=(0.0, 0.0))

def test_beam_support_out_of_bounds_negative():
    with pytest.raises(ValueError, match="Support location must be within beam limits"):
        Beam(length=10.0, supports=(-1.0, 10.0))

def test_beam_support_out_of_bounds_excessive():
    with pytest.raises(ValueError, match="Support location must be within beam limits"):
        Beam(length=10.0, supports=(0.0, 12.0))

def test_beam_representation():
    beam = Beam(length=5.0, supports=(0.0, 5.0))
    assert str(beam) == "Beam(length=5.0 m, supports=(0.0, 5.0))"
