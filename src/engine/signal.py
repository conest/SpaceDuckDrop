from typing import Callable


class Signal:
    active: bool = False
    name: str = "Signal"
    source: str = ""
    data: list = []
    '''Data of signal source, for emit to target function'''

    def __init__(self, name: str, source: str):
        self.name = name
        self.active = False
        self.source = source
        self.data: list = []

    def __str__(self) -> str:
        return f'[Signal] name: {self.name}'

    def inactive(self):
        self.active = False


class Link:
    signal: Signal
    target = None
    targetFunc: Callable

    def __init__(self, source: Signal, target, targetFunc: Callable):
        self.signal = source
        self.target = target
        self.targetFunc = targetFunc

    def __str__(self) -> str:
        return f'[Link] signal: {self.signal} target: {self.target}'

    def signal_active(self) -> bool:
        return self.signal.active

    def call_target(self):
        self.signal.inactive()
        self.targetFunc(self.target, self.signal.data)


class SignalGroup:
    signals: dict = {}

    def __init__(self):
        self.signals = {}

    def sign(self, s: Signal):
        self.signals[s.name] = s

    def active(self, name: str):
        if name in self.signals:
            self.signals[name].active = True

    def inactive(self, name: str):
        if name in self.signals:
            self.signals[name].active = False

    def check(self, name: str) -> Signal:
        '''Only return actived signal'''
        if name in self.signals and self.signals[name].active:
            return self.signals[name]
        return None

    def consume(self, name: str) -> Signal:
        if name in self.signals:
            self.signals[name].active = False
            return self.signals[name]
        return None

    def get(self, name: str) -> Signal:
        if name in self.signals:
            return self.signals[name]
        return None
