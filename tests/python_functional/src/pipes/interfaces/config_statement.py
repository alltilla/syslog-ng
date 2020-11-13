class ConfigStatement(object):
    def __init__(self, driver_name, options):
        self.driver_name = driver_name
        self.options = options

    def render(self):
        config_repr = "%s (\n" % self.driver_name
        for option_name, option_name_value in self.options.items():
            config_repr += "  %s(%s)\n" % (option_name, option_name_value)
        config_repr += ");"
        return config_repr
