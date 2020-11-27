from src.pipes.sources.source import Source
from src.pipes.interfaces.config_statement import ConfigStatement

class ExampleMsgGeneratorSource(Source):
    DEFAULT_MESSAGE = "-- Generated message. --"

    def __init__(self, **options):
        self.__config = ConfigStatement("example-msg-generator", options)
        super(ExampleMsgGeneratorSource, self).__init__()

    @property
    def config(self):
        return self.__config

    @property
    def stats(self):
        raise NotImplementedError

    @property
    def entrypoint(self):
        raise NotImplementedError
