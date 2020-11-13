from src.syslog_ng_config.renderer import render_driver_options

class ConfigStatement(object):
    def __init__(self, driver_name, options):
        self.driver_name = driver_name
        self.options = options

    def render(self):
        config_repr = "%s (\n" % self.driver_name
        config_repr += render_driver_options(self.options)
        config_repr += ");"
        return config_repr
