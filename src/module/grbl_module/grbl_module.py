import functools
import time
from typing import Dict

from pubsub import pub

from src.util import logger

from ..builder import build_grbl_settings



from .grbl_position_parser import (
    GrblStatus,
    GrblStatusQueryParser,
)


from ..communication import Response
from ..components import ModuleComponent
from ..module import Module


class GrblModule(Module):
    """GrblModule encapsulate the functions to interact with grbl firmware

    Attributes
    -----------
        ack_str : str
            acknowledgement string returned from the microcontroller
        eof : str
            grbl eof attached to every command

    """

    unknown_position: float = (
        0.0  # if position is 0.0, grbl module is in non deterministic state
    )

    def __init__(self, module_component: ModuleComponent):
        """Init the GrblModule
         Parameters
        ----------
        module_component : ModuleComponent

        """
        eol: str = "\n"
        ack_str: str = "ok" + eol
        Module.__init__(self, eol, ack_str, module_component)

        self._current_step_feed_rate = 0.0

        self._grbl_status: GrblStatus = GrblStatus(0.0, 0.0, "Alarm")

    async def set_settings(self, value=""):
        settings = build_grbl_settings(self._module_name)
        result = []
        for key, value in settings.items():
            setting = key + "=" + str(value)
            response_result: Response = await self._client.send_message_ack(
                setting + self._eol, number_of_response=1
            )
            result.append(response_result[0].result)

        return all(result)

    async def get_settings(self, value=""):
        settings_command: str = self._commands["get_settings"]
        result = []
        response_result: Response = await self._client.send_message_ack(
            settings_command + self._eol, number_of_response=34
        )
        settings = {}
        for response in response_result:
            if response.result:
                message = response.message.split("=")
                settings[message[0]] = message[1]

        return settings

    async def home(self, value: str = ""):
        """This method send homing command: $H to grbl module

        Parameters
        ----------
        value : str
            value is empty string

        Returns
        ---------
        response : Response
            Response from the communication client

        """
        home_command: str = self._commands["home"]
        # 1await self.reset_grbl()
        logger.info("homing {}".format(self._module_name))
        result = await self._client.send_message_ack(
            home_command + self._eol, number_of_response=1, timeout=60
        )
        await self._update_current_status()
        return result[0].result

    async def reset_grbl(self, value: str = ""):  # change to emergency stop?
        """
        resets grbl, sending special character Ctrl-x (this stops motors)

        Parameters
        ----------
        value : str
            value is empty string


        """
        reset_result: bool = True
        try:
            reset_command: str = self._commands["reset"]
            logger.trace(
                "{}: send reset:{} command".format(self._module_name, reset_command)
            )
            result = await self._client.send_message_ack(
                reset_command + self._eol, number_of_response=5
            )
            for r in result:
                logger.trace(r.message)
                if not r.result:
                    reset_result = False

        except Exception as e:
            logger.critcial("Couldn't reset grbl due to {}".format(str(e)))
            reset_result = False
        return reset_result

    async def reset_unlock(self, value: str = ""):
        """The function enable us to check the reset the grbl module and check the status of the grbl
        module
        """

        await self.reset_grbl()

        position, state = await self.get_x_position_state()
        logger.trace("position : {} state: {}".format(position, state))

        if position == self.unknown_position:
            logger.critical("Grbl module is in non deterministic state. Perform homing")
            result = False
        else:
            result = await self.__unlock()
        return result

    async def query_status(
        self,
    ) -> str:  # TODO error handling while querying status. Grbl module may be resetted automatically and go into alarm state
        """This method query the current status of the grbl module

        Returns
        --------
        grbl status: str
            status of the grbl \n
            Example <Idle|MPos:-200.000,5.000,0.000|FS:0,0|WCO:0.000,0.000,0.000>

        """

        get_position_command: str = self._commands["get_position"]
        grbl_status: str = ""
        logger.trace(
            "{}: query position:{} command".format(
                self._module_name, get_position_command
            )
        )
        result = await self._client.send_message_ack(
            get_position_command, number_of_response=1
        )
        logger.trace(
            "{}: query position:{} command response {}".format(
                self._module_name, get_position_command, result
            )
        )
        if result[0].result:
            grbl_status = result[0].message

        return grbl_status

    async def __unlock(self, value="unlock") -> bool:
        """unlock the grbl module
        Caution: send unlock only after resetting. Do not perform unlock without resetting.
        """
        result: bool = False
        logger.info("unlocking grbl module")
        unlock_command = self.get_command(value)
        response: Response = await self._client.send_message_ack(
            unlock_command + self._eol, 2
        )

        for r in response:
            logger.trace(
                "{}: recevied response:{} command: {}".format(
                    self._module_name, unlock_command, r.message
                )
            )

        return response[1].result

    async def get_state(self):
        state = ""
        await self._update_current_status()
        if self._grbl_status is not None:
            state = self._grbl_status.state
        return state

    async def _update_current_status(
        self, query_count: int = 1
    ) -> Dict[str, float | str]:
        """run this command after every step to update the current state, position of the grbl module"""
        status_str = await self.query_status()
        query_parser = GrblStatusQueryParser(status_str)
        self._grbl_status = query_parser.get_status()
        retry = 3
        if self._grbl_status is not None:
            logger.trace("publishing grbl status {}".format(self._grbl_status))
            pub.sendMessage(
                self._module_name,
                grbl_status={
                    "module_name": self._module_name,
                    "status": self._grbl_status,
                },
            )

        elif query_count <= retry:
            logger.warning(
                "{} received invalid query status string:  {}".format(
                    self._module_name, status_str
                )
            )
            logger.warning(
                "Retrying to get the grbl module {} status {} times".format(
                    self._module_name, query_count
                )
            )
            await self._update_current_status(query_count + 1)
        else:
            logger.warning(
                "Stop the program and check for the error in {}".format(
                    self._module_name
                )
            )

    async def _get_position_state(self, axis: str):
        """This method extract the position, state from the status message

        Parameters
        -----------
            axis : str
                required axis position to be extracted.

        Returns
        ---------
            grbl_position : float
                position of the grbl X,Y
            grbl_state : float
                current state of the grbl Example: Idle, Home, Run, Warn

        """
        grbl_position: float | None = None
        grbl_state: str = ""
        await self._update_current_status()
        if self._grbl_status is None:
            logger.critical(
                "Critical error in grbl module {}".format(self._module_name)
            )
        else:
            grbl_state = self._grbl_status.state
            grbl_position = self._grbl_status.__getattribute__(axis)

        return (grbl_position, grbl_state)

    get_x_position_state = functools.partialmethod(_get_position_state, axis="X")
    get_y_position_state = functools.partialmethod(_get_position_state, axis="Y")
    get_y_position_state.__doc__ = _get_position_state.__doc__
    get_x_position_state.__doc__ = _get_position_state.__doc__

    async def _get_state(self, value: str) -> str:
        """This method extract the state of the grbl module

        Parameters
        -----------
        value: str
            empty string

        Returns
        -------------
        str

        """
        get_position_command: str = self._commands["get_position"]
        logger.trace(
            "{}: send position:{} command".format(
                self._module_name, get_position_command
            )
        )
        grbl_status = await self._client.send_message_ack(
            get_position_command, number_of_response=1
        )
        query_parser = GrblStatusQueryParser(grbl_status)
        grbl_state = query_parser.get_state()
        return grbl_state

    async def gcode(self, value):
        """process gcode

        Parameters
        ----------
        value: str
            gcode str
        Returns
        -------
        Response

        """
        logger.trace("Gcode is processed here {}".format(value))
        result: bool = True
        gcode_name, command_list, value_list = value
        gcode_dict: Dict[str, float] = {}
        for command, command_value in zip(command_list, value_list):
            command_letter = self._commands.get(command, "")
            check_command_letter = lambda: command_letter in ["X", "Y", "Z"]
            if (
                check_command_letter() and command_value > 0
            ):  # check and change the sign to negative  only for motion commands and not for speed
                command_value = -command_value

            gcode_dict[self._commands.get(command, "")] = round(command_value, 2)

        gcode_str = gcode_name

        for key, value in gcode_dict.items():
            gcode_str += " " + key + str(value)

        logger.info(gcode_str)
        result = await self._client.send_message_ack(
            gcode_str + self._eol, number_of_response=1
        )

        if "move_check" in command_list:
            result = await self.check_target_x_position(value=gcode_dict["X"])
            pass

        if "rotate_check" in command_list:
            result = await self.check_target_y_position(value=gcode_dict["Y"])
            pass

        return result

    async def _new_position(
        self, axis: str, soft_limit_param: str, value: float
    ) -> bool:  # TODO check maximum movable/rotable soft limit
        """sends new position command to grbl based on axis

        Parmaeters
        -----------
        axis: str
            axis - X,Y

        soft_limit_param: str
            the name of the soft_limit_param from the configuration file

        value: float
            position to which grbl module has to be moved or rotated

        Returns
        ---------
        bool

        """
        change_sign: float = (
            lambda value: -value if value >= 0 else value
        )  # change the sign of lambda
        value = change_sign(value)
        value = round(value, 2)
        new_position_command: str = self._commands[axis] + str(value)
        logger.trace(
            "{}: send position:{} command".format(
                self._module_name, new_position_command
            )
        )
        response = await self._client.send_message_ack(
            new_position_command + self._eol, 1
        )
        logger.trace(
            "{}: recevied position:{} command: {}".format(
                self._module_name, new_position_command, response
            )
        )
        if "ok" in response[0].message:
            return True  # TODO check for other messages like O or k or unicode
        return False

    #: move the grbl module to desired position

    move = functools.partialmethod(
        _new_position, axis="move", soft_limit_param="x_max_travel"
    )

    move.__doc__ += _new_position.__doc__
    #: rotate the grbl module to desired position

    rotate = functools.partialmethod(
        _new_position, axis="rotate", soft_limit_param="y_max_travel"
    )
    rotate.__doc__ += _new_position.__doc__

    async def _check_target_position(self, axis: str, value: float):
        """This method checks whether the grbl module reached its target position

        Parameters
        -----------
        axis: str
            axis of the grbl module

        value: str
            target value which is required to be reached by grbl axis


        Returns
        --------
        bool

        """

        change_sign: float = (
            lambda value: -value if value >= 0 else value
        )  # change the sign of lambda
        value = change_sign(value)
        value = round(value, 2)
        result: bool = False
        while True:
            try:
                position, state = await self._get_position_state(axis)
                check_position: bool = lambda position: abs(position) == abs(value)
                check_state_position: bool = (
                    lambda state, position: state == "Idle"
                    and abs(position) != abs(value)
                )  # when the grbl is in Idle state and target position not reached

                result = check_position(position)
                if result:
                    break
                result = check_state_position(state, position)
                if result:
                    result = False
                    break
                time.sleep(
                    0.5
                )  # recommended sleeping cycle before sending position command to grebl. 5Hz or 10Hz
            except Exception as e:
                logger.warning(
                    "Exception raised during getting position {}".format(str(e))
                )
                result = False
        return result

    check_target_x_position = functools.partialmethod(_check_target_position, axis="X")
    check_target_y_position = functools.partialmethod(_check_target_position, axis="Y")

    async def move_check(self, value):
        """This method send move command and wait until the target position is reached

        Parameters
        -----------
        value: float
            target value which is required to be reached by grbl axis


        Returns
        --------
        bool

        """
        result = await self.move(value=value)
        if result:
            result = await self.check_target_x_position(value=value)

        # await self.check_target_x_position(value = value)
        return result

    async def rotate_check(self, value):
        """This method send rotate command and wait until the target position is reached

        Parameters
        -----------
        value: float
            target value which is required to be reached by grbl axis


        Returns
        --------
        bool

        """
        result = await self.rotate(value=value)
        if result:
            result = await self.check_target_y_position(value=value)
        return result
