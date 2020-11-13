from src.pipes.destinations.destination import Destination
from src.pipes.interfaces.config_statement import ConfigStatement
from src.pipes.interfaces.io import Endpoint
from src.common.operations import wait_for_file_creation
from src.common.operations import open_file


class FileDestinationEndpoint(Endpoint):
    def __init__(self, path):
        self.path = path
        self.file = None
        super(FileDestinationEndpoint, self).__init__()

    def __del__(self):
        if self.file:
            self.file.close()

    def open_file(self):
        if not wait_for_file_creation(self.path)
            raise Exception("File has not been created in time: {}".format(self.path))
        self.file = open_file(self.path)

    def read_log(self, content, counter=1):
        if self.file is None:
            self.open_file()

        data = ""
        with open_file(self.path, "r") as f:
            for _ in range(counter):
                data += f.readline()
        return data


class FileDestinationConfigStatement(ConfigStatement):
    def __init__(self, path, options):
        self.set_path(path)
        super(FileDestinationConfigStatement, self).__init__("file", options)

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    def render(self):
        config_snippet = "file (\n"
        config_snippet += "  '{}'\n".format(self.get_path())
        for option_name, option_name_value in self.options.items():
            config_snippet += "  {}({})\n".format(option_name, option_name_value)
        config_snippet += ");"
        return config_snippet


class FileDestination(Destination):
    def __init__(self, file_name, **options):
        config = FileDestinationConfigStatement(file_name, options)
        stats = DestinationStats(config.driver_name, config.get_path())
        endpoint = FileDestinationEndpoint(config.get_path())
        super(FileDestination, self).__init__(config, stats, endpoint)
