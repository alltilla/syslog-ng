from src.pipes.pipe import Pipe


class Source(Pipe):
    def __init__(self, config, stats, entrypoint):
        self.group_type = "source"
        self.config = config
        self.stats = stats
        self.entrypoint = entrypoint
        super(Source, self).__init__(self.config, self.stats)

    def copy_entrypoint(self):
        pass
