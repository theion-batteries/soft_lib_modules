import re
from dataclasses import dataclass
from typing import Callable, Dict

from theion_device.util import logger


@dataclass
class GrblStatus:
    X: float | None
    Y: float | None
    state: str | None


class GrblStatusQueryParser:
    """GrblStatusQueryParaser is used to parse the query string and extract useful inforamtion"""

    def __init__(self, position_str: str):
        # TODO check for unicode
        """
        Parameters:
        ----------
        position_str: str

        """
        self._position_str = position_str
        logger.trace("Received position string is {}".format(self._position_str))

        self.postition: Dict[str, Callable] = {
            "X": self.get_x_position,
            "Y": self.get_y_position,
        }

    def get_status(self) -> GrblStatus:
        """This method is used to get the status

        Returns
        --------
        GrblStatus

        """

        status: GrblStatus = None
        try:
            position_x = self.get_x_position()
            position_y = self.get_y_position()
            state = self.get_state()
            status = GrblStatus(position_x, position_y, state)
        except AttributeError as e:
            logger.error("Attribute error in getting status")
            status = None
        logger.trace(status)
        return status

    def get_x_position(self):
        """This method is used to parse X postion from the position string"""
        position_x: float | None = None
        position_str = re.search("MPos:(.*),(.*)", self._position_str).group()
        if len(position_str) == 0:
            position_x = None
        else:
            first_colon_index = position_str.find(":")
            first_comma_index = position_str.find(",")

            if first_colon_index != -1 and first_comma_index != -1:
                position_x = position_str[first_colon_index + 1 : first_comma_index]

        return float(position_x)

    def get_y_position(self):
        """This method is used to parse Y postion from the position string"""
        position_y: float | None = None
        position_str = re.search("MPos:(.*),(.*)", self._position_str).group()
        if len(position_str) == 0:
            position_y = None  # TODO implement the alternation
        else:
            first_comma_index = position_str.find(",")
            second_comma_index = position_str.find(",", first_comma_index + 1)

            if first_comma_index != -1 and second_comma_index != -1:
                position_y = position_str[first_comma_index + 1 : second_comma_index]
        return float(position_y)

    def get_state(self):
        """
        extract the state of the module from the grbl module

        Return
        ------
            str
        """
        grbl_state: str | None = ""
        try:
            grbl_state = ""
            first_index = self._position_str.find("<")
            second_index = self._position_str.find("|")
            if first_index != -1 and second_index != -1:
                grbl_state = self._position_str[first_index + 1 : second_index]
            logger.trace("grbl state {}".format(grbl_state))
        except AttributeError as e:
            logger.error("Attribute error in getting state")
            grbl_state = None
        return grbl_state
