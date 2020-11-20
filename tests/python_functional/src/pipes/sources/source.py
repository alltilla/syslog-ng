from src.pipes.pipe import Pipe
from abc import abstractmethod


class Source(Pipe):
    def __init__(self):
        self.group_type = "source"
        super(Source, self).__init__()

    @property
    @abstractmethod
    def entrypoint(self):
        pass

    def copy_entrypoint(self):
        pass
