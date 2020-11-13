import src.testcase_parameters.testcase_parameters as tc_parameters
from src.syslog_ng_ctl.syslog_ng_ctl import SyslogNgCtl


class Stats(object):
    def __init__(self, component_type, driver_name, instance, counters):
        self.component = "{}.{}.{}".format(component_type, driver_name, instance)
        self.counters = counters
        self.syslog_ng_ctl = SyslogNgCtl(tc_parameters.INSTANCE_PATH)

    def build_query_pattern(self):
        return "{}{}".format(self.component, '.')

    def build_stats_pattern(self):
        return "{}{}".format(self.component, ',')

    def parse_result(self, result, result_type):
        parsed_output = {}
        for counter in self.counters:
            for line in result:
                if counter in line:
                    if result_type == "query":
                        parsed_output.update({counter: int(line.split(".")[-1].split("=")[-1])})
                    elif result_type == "stats":
                        parsed_output.update({counter: int(line.split(".")[-1].split(";")[-1])})
                    else:
                        raise Exception("Unknown result_type: {}".format(result_type))
        return parsed_output

    def get_query(self):
        query_pattern = self.build_query_pattern()
        query_result = self.syslog_ng_ctl.query(pattern="*{}*".format(query_pattern))['stdout'].splitlines()

        return self.parse_result(result=query_result, result_type="query")

    def get_stats(self):
        stats_pattern = self.build_stats_pattern()
        stats_result = self.syslog_ng_ctl.stats()['stdout'].splitlines()

        return self.parse_result(result=stats_result, result_type="stats")


class SourceStats(Stats):
    def __init__(self, driver_name, instance):
        counters = ["processed", "stamp"]
        super(SourceStats, self).__init__("src", driver_name, instance, counters)


class DestinationStats(Stats):
    def __init__(self, driver_name, instance):
        counters = ["processed", "written", "dropped", "memory_usage", "queued"]
        super(DestinationStats, self).__init__("dst", driver_name, instance, counters)
