from abc import ABC, abstractmethod


class Pipe(ABC):
    @property
    @abstractmethod
    def config(self):
        pass

    @property
    @abstractmethod
    def stats(self):
        pass
