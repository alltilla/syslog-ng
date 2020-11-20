from abc import ABC, abstractmethod

class Entrypoint(ABC):
    @abstractmethod
    def write_log(self, content):
        pass

    @abstractmethod
    def write_logs(self, contents):
        pass


class Endpoint(ABC):
    @abstractmethod
    def read_log(self):
        pass

    @abstractmethod
    def read_logs(self, counter):
        pass
