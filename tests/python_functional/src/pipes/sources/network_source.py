from src.pipes.sources.source import Source
from src.pipes.interfaces.config_statement import ConfigStatement
from src.pipes.interfaces.stats import SourceStats
from src.pipes.interfaces.io import Entrypoint

from src.helpers.loggen.loggen import Loggen

from src.common.operations import sanitize
from src.common.operations import open_file
from src.common.random_id import get_unique_id

import src.testcase_parameters.testcase_parameters as tc_parameters

from pathlib2 import Path

class NetworkEntrypoint(Entrypoint):
    def __init__(self, transport, ip, port):
        self.ip = ip
        self.port = port
        self.transport = transport
        super(NetworkEntrypoint, self).__init__()

    def write_log(self, content, rate=None):
        loggen_input_file_path = str(Path(tc_parameters.WORKING_DIR, "loggen_input_{}.txt".format(get_unique_id())))
        with open_file(loggen_input_file_path, mode="w") as f:
            f.write(content)

        Loggen().start(self.ip, self.port, read_file=str(loggen_input_file_path), dont_parse=True, permanent=True, rate=rate, **self.transport_to_loggen_params())

    def transport_to_loggen_params(self):
        mapping = {
            "tcp": {"inet": True, "stream": True},
            "udp": {"dgram": True},
            "tls": {"use_ssl": True},
            "proxied-tcp": {"inet": True, "stream": True},
            "proxied-tls": {"use_ssl": True},
        }
        return mapping[self.transport]


class NetworkConfigStatement(ConfigStatement):
    def __init__(self, options):
        super(NetworkConfigStatement, self).__init__("network", options)

    def get_transport_or_default(self):
        transport = self.options["transport"] if "transport" in self.options else "tcp"
        return sanitize(transport)

    def get_ip_or_default(self):
        return self.options["ip"] if "ip" in self.options else "localhost"

    def get_port_or_default(self):
        mapping = {
                "udp": 514,
                "tcp": 601,
                "tls": 6514,
            }
        return self.options["port"] if "port" in self.options else mapping[self.get_transport_or_default()]


class NetworkSource(Source):
    def __init__(self, **options):
        config = NetworkConfigStatement(options)
        stats = None
        entrypoint = NetworkEntrypoint(config.get_transport_or_default(), config.get_ip_or_default(), config.get_port_or_default())
        super(NetworkSource, self).__init__(config, stats, entrypoint)