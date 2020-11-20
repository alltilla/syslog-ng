from abc import ABC, abstractmethod

class Entrypoint(ABC):
    @abstractmethod
    def write_log(self, content):
        pass

    def write_logs(self, contents):
        for content in contents:
            self.write_log(content)


class Endpoint(ABC):
    @abstractmethod
    def read_log(self):
        pass

    @abstractmethod
    def read_logs(self, counter):
        pass
