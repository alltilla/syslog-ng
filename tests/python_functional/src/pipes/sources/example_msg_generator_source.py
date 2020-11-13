from src.pipes.sources.source import Source
from src.pipes.interfaces.config_statement import ConfigStatement

class ExampleMsgGeneratorSource(Source):
    DEFAULT_MESSAGE = "-- Generated message. --"

    def __init__(self, **options):
        config = ConfigStatement("example-msg-generator", options)
        stats = None
        entrypoint = None
        super(ExampleMsgGeneratorSource, self).__init__(config, stats, entrypoint)