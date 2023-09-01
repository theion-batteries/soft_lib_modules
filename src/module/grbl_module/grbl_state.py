from statemachine import State, StateMachine

from definitions import logger

"""
Alarm - Homing enabled but homing cycle not run or error has been detected such as limit switch activated. Home or unlock to resume.

Idle - Waiting for any command.

Jog - Performing jog motion, no new commands until complete, except Jog commands.

Homing -Performing a homing cycle, won’t accept new commands until complete.

Check - Check mode is enabled; all commands accepted but will only be parsed, not executed.

Cycle - Running GCode commands, all commands accepted, will go to Idle when commands are complete.

Hold - Pause is in operation, resume to continue.

Safety Door - The safety door switch has been activated, similar to a Hold but will resume on closing the door. You probably don’t have a safety door on your machine!

Sleep - Sleep command has been received and executed, sometimes used at the end of a job. Reset or power cycle to continue."""


class GrblState(StateMachine):
    start = State(initial=True)
    connected = State()
    disconnected = State()
    # alarm = State()
    idle = State()
    run = State()
    home = State()
    # hold = State()
    # jog = State()
    # sleep = State()
    connection_error = State()

    connection_sucess = start.to(connected)
    connection_failure = start.to(connection_error)
    close_connection = connected.to(disconnected)
    """
    When to Home
        - on new connection
        - on complete reset

    status query report give - Alarm and Mpos = 0
    It is dangerous to reset the grb when it is in Alarm and Mpos = 0.0.
    """

    connected_to_home = connected.to(home)
    idle_to_home = idle.to(home)
    """
    Homing state is present for microseconds. The GRBL module quickly change from homing to
    idle state
    """
    homing_completed = home.to(idle)

    displacement = idle.to(run)
    complete_displacement = run.to(idle)

    rotate = start.to(run)
    complete_rotation = run.to(idle)
    """
    on Reset:
      - send unlock command $X along with reset
    """
    """def on_enter_connected(self):
        logger.info("Module entered connected state")
        return True

    def on_exit_start(self):
        logger.info("Module is no longer in start state")"""
