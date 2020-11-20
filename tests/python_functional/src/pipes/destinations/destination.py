from src.pipes.pipe import Pipe
from abc import abstractmethod

class Destination(Pipe):
    def __init__(self):
        self.group_type = "destination"
        super(Destination, self).__init__()

    @property
    @abstractmethod
    def endpoint(self):
        pass

    def copy_endpoint(self):
        pass
