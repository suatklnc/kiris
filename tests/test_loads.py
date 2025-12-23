import pytest
from beam_analysis.loads import PointLoad, UDL, PointMoment


def test_point_load_initialization():
    load = PointLoad(force=10.0, location=2.5)
    assert load.force == 10.0
    assert load.location == 2.5


def test_point_load_invalid_location():
    with pytest.raises(ValueError):
        PointLoad(force=10.0, location=-1.0)


def test_udl_initialization():
    load = UDL(magnitude=5.0)
    assert load.magnitude == 5.0


def test_udl_representation():
    load = UDL(magnitude=5.0)
    assert str(load) == "UDL(magnitude=5.0 kN/m)"


def test_point_load_representation():
    load = PointLoad(force=10.0, location=2.5)
    assert str(load) == "PointLoad(force=10.0 kN, location=2.5 m)"


def test_point_moment_initialization():
    load = PointMoment(moment=10.0, location=5.0)
    assert load.moment == 10.0
    assert load.location == 5.0


def test_point_moment_representation():
    load = PointMoment(moment=10.0, location=5.0)
    assert str(load) == "PointMoment(moment=10.0 kNm, location=5.0 m)"
