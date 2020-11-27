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


class ServerEndpoint(Endpoint):
    def __del__(self):
        if self.is_running:
            self.stop()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @property
    @abstractmethod
    def is_running(self):
        pass
