from src.pipes.pipe import Pipe


class Destination(Pipe):
    def __init__(self, config, stats, endpoint):
        self.group_type = "destination"
        self.endpoint = endpoint
        super(Destination, self).__init__(config, stats)

    def copy_endpoint(self):
        pass
