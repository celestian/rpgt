from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def update(self, payload):
        raise NotImplementedError


class Subject:

    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def unregister_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, payload):
        for observer in self._observers:
            observer.update(payload)
