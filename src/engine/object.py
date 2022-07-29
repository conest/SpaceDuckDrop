from .signal import SignalGroup


class Object:
    name: str
    '''Object.name: work as an unique ID'''
    signals: SignalGroup

    def __init__(self):
        self.name = "Default_Object_Name"
        self.signals = SignalGroup()
        self.attribute = {}
        self.hitbox = None

    def __str__(self) -> str:
        return f'[Object] {self.name}'

    def update(self, _delta: int):
        pass
