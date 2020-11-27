from src.pipes.destinations.destination import Destination
from src.pipes.interfaces.stats import DestinationStats
from src.pipes.interfaces.config_statement import ConfigStatement
from src.pipes.interfaces.io import ServerEndpoint
from src.executors.snmptrapd import SNMPtrapd
# from src.common.blocking import wait_until_true

# import src.testcase_parameters.testcase_parameters as tc_parameters


class SnmpDestinationEndpoint(ServerEndpoint):
    def __init__(self, port):
        self.__snmptrapd = SNMPtrapd(port)
        self.__is_running = False
        super(SnmpDestinationEndpoint, self).__init__()

    def start(self):
        self.__is_running = self.__snmptrapd.start()

    def stop(self):
        self.__snmptrapd.stop()
        self.__is_running = False

    @property
    def is_running(self):
        return self.__is_running

    def read_log(self, timeout=SNMPtrapd.DEFAULT_TIMEOUT):
        return self.read_logs(1, timeout=timeout)[0]

    def read_logs(self, counter, timeout=SNMPtrapd.DEFAULT_TIMEOUT):
        if not self.__is_running:
            raise Exception("snmptrapd is not started.")
        return self.__snmptrapd.get_traps(counter, timeout=timeout)



class SnmpDestination(Destination):
    def __init__(self, **options):
        self.__config = ConfigStatement("snmp", options)
        self.__endpoint = SnmpDestinationEndpoint(self.__config.options["port"])
        self.__stats = None

        super(SnmpDestination, self).__init__()

    @property
    def config(self):
        return self.__config

    @property
    def endpoint(self):
        return self.__endpoint

    @property
    def stats(self):
        return self.__stats
