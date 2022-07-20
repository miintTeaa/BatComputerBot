command_list = {}

class Command:
  def __init__(self, name, function, arg_min, arg_max):
    self.name = name
    self.function = function
    self.arg_min = arg_min
    self.arg_max = arg_max
    command_list[self.name] = self