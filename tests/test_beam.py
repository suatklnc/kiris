import pytest
from beam_analysis.beam import Beam, Support, SupportType


def test_beam_initialization():
    supports = [Support(0.0, SupportType.PINNED), Support(10.0, SupportType.ROLLER)]
    beam = Beam(length=10.0, supports=supports)
    assert beam.length == 10.0
    assert beam.supports == supports


def test_beam_invalid_length():
    with pytest.raises(ValueError, match="Length must be positive"):
        Beam(length=-5.0, supports=[Support(0.0), Support(5.0)])


def test_beam_zero_length():
    with pytest.raises(ValueError, match="Length must be positive"):
        Beam(length=0.0, supports=[Support(0.0)])


def test_beam_support_out_of_bounds_negative():
    with pytest.raises(ValueError, match="Support location must be within beam limits"):
        Beam(length=10.0, supports=[Support(-1.0)])


def test_beam_support_out_of_bounds_excessive():
    with pytest.raises(ValueError, match="Support location must be within beam limits"):
        Beam(length=10.0, supports=[Support(12.0)])


def test_beam_representation():
    beam = Beam(length=5.0, supports=[Support(0.0, SupportType.PINNED), Support(5.0, SupportType.ROLLER)])
    assert str(beam) == "Beam(length=5.0 m, supports=[PINNED at 0.0m, ROLLER at 5.0m])"
