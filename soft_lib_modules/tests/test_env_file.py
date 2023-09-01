import os

import pytest
from omegaconf import OmegaConf

from soft_lib_modules.definitions import STEP_DIR, logger

OmegaConf.register_new_resolver("eval", eval)


@pytest.fixture
def env():
    environment_file = "environment.yaml"
    file_path = os.path.join(STEP_DIR, environment_file)
    env = OmegaConf.load(file_path)

    return env


def test_ph_total_rotation(env):
    total_rotation = env["cooling"]["ph_total_rotation"]
    number_of_rotation = env["cooling"]["number_of_rotation"]
    turn_head = env["cooling"]["turn_head"]
    ph_rotation = env["cooling"]["ph_first_rotation"]

    assert total_rotation == turn_head * number_of_rotation


def test_whs_position(env):
    cooling_whs_position = env["cooling"]["whs_position"]
    sinking_whs_position = env["whs_motion"]["X"]
    cooling_safe_distance = env["cooling"]["safe_distance"]
    alignment_safe_distance = env["alignment"]["safe_distance"]
    alignment_whs_position = env["alignment"]["whs_position"]
    logger.trace(alignment_whs_position)
    assert sinking_whs_position - cooling_safe_distance == cooling_whs_position
    assert sinking_whs_position - alignment_safe_distance == alignment_whs_position


def test_pcb_above_sulphur(env):
    buffer_distance = env["extraction"]["buffer_distance"]
    pcb_distance = env["extraction"]["pcb_distance"]
    pcb_exposed = env["extraction"]["pcb_exposed"]
    pcb_above_sulphur = env["extraction"]["pcb_above_sulphur_distance"]
    logger.trace(pcb_above_sulphur)
    assert pcb_above_sulphur == pcb_distance - pcb_exposed + buffer_distance


def test_pcb_above_sulphur(env):
    ph_distance = env["cooling"]["ph_first_cooling_rotation_position"]
    logger.trace(ph_distance)


def test_extraction_position(env):
    whs_extraction_position = env["extraction"]["slow_extraction_whs_position"]
    ph_extraction_position = env["extraction"]["slow_extraction_ph_x_position"]
    logger.trace(whs_extraction_position)
    logger.trace(ph_extraction_position)
