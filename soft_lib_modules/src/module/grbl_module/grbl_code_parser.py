import tokenize

from .grbl_module import GrblModule


class GrblGCodeParser:
    def __init__(self, gcode_str: str = ""):
        self.gcode_list = tokenize.generate_tokens(
            gcode_str,
        )

    def parse_gcode(self, module: GrblModule):
        pass
