import logging

import pytest

from soft_lib_modules.src.module.grbl_module.grbl_position_parser import GrblStatusQueryParser


@pytest.fixture
def position():
    position_str = "<Idle|MPos:-200.000,5.000,0.000|FS:0,0|WCO:0.000,0.000,0.000>\n"
    position = GrblStatusQueryParser(position_str)
    return position.get_status()


@pytest.fixture
def wrong_position():
    position_str = "<Idle"
    position = GrblStatusQueryParser(position_str)

    return position.get_status()


# test grbl position assigned
def test_grbl_x_position(position):
    assert position.X == -200.0


def test_grbl_y_position(position):
    assert position.Y == 5


def test_grbl_state_position(position):
    assert position.state == "Idle"


def test_grbl_query_status(position):
    assert position.X == -200.00
    assert position.Y == 5
    assert position.state == "Idle"


def test_grbl_query_status(wrong_position):
    status = wrong_position
    assert status is None
