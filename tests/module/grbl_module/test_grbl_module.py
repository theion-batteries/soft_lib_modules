from theion_device.module.grbl_module import GrblModule


def test_build_grbl_module():
    module = GrblModule("cnt_motion")
    assert module
