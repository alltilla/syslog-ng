from enum import Enum, auto


class ParamMode(Enum):
  CONCAT = auto()
  APPEND = auto()
  SET = auto()


def build_args_for_executor(possible_params, ignore_params, **params):
  args = []

  for param_name, param_value in params.items():
    if param_name in ignore_params or param_value is None:
      continue

    param_prefix, param_mode = possible_params[param_name]

    if param_mode == ParamMode.CONCAT:
      param = [ param_prefix + str(param_value) ]
    elif param_mode == ParamMode.APPEND:
      param = [ param_prefix, str(param_value) ]
    elif param_mode == ParamMode.SET:
      if param_value is True:
        param = [ param_prefix ]
    else:
      raise Exception("Invalid ParamMode for '{}': {}".format(param_name, str(param_mode)))

    args.extend(param)

  return args
