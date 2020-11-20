from src.pipes.destinations.destination import Destination
from src.pipes.interfaces.stats import DestinationStats
from src.pipes.interfaces.config_statement import ConfigStatement
from src.pipes.interfaces.io import Endpoint
from src.driver_io.file.file import File
from src.common.blocking import wait_until_true

import src.testcase_parameters.testcase_parameters as tc_parameters
from pathlib2 import Path


class FileDestinationEndpoint(Endpoint):
    def __init__(self, path):
        self.file = File(path)
        super(FileDestinationEndpoint, self).__init__()

    def read_log(self):
        if not self.file.is_opened():
            if not self.file.wait_for_creation():
                raise Exception("File destination's output file was not created in time.")
            self.file.open("r")

        return wait_until_true(self.file.read)

    def read_logs(self, counter):
        content = []

        while len(content) != counter:
            buffer = self.read_log()
            if buffer:
                content.append(buffer)

        return content


class FileDestinationConfigStatement(ConfigStatement):
    def __init__(self, path, options):
        self.set_path(path)
        super(FileDestinationConfigStatement, self).__init__("file", options)

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = str(Path(tc_parameters.WORKING_DIR, path))

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
