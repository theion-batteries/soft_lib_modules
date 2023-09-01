from statemachine import State, StateMachine


class ClientState(StateMachine):
    start = State(initial=True)
    connected = State()
    fail = State()
    disconnected = State()
    stop = State()
    waiting = State()
    closing = State()
