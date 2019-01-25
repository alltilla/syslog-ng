import re
import subprocess

class Command:
  def __init__(self, token, keywords, types, grep_list):
    self.token = token
    self.keywords = keywords
    self.types = types
    self.grep_list = grep_list

  def get_grep_list(self):
    try:
      grep_list = subprocess.check_output("git grep -h " + self.token, stderr=subprocess.STDOUT, shell=True)
    except:
      print("Error in grep")
      return
    self.grep_list = grep_list.decode().split("\n")

  def find_keywords(self):
    keywords = []
    for line in self.grep_list:
      if re.match(r'^\s*{\s*"\w+",\s*' + self.token + r'+[\s,}]+', line):
        keywords.append(re.findall(r"\w+", line)[0])
    self.keywords = list(set(keywords))
  
  def find_types(self):
    types = []
    for line in self.grep_list:
      if re.match(".*" + self.token + r"\s*'\('\s*\w+", line):
        types.append(re.findall(r"\w+", line)[1])
      elif re.match(".*" + self.token + r".*}\s+\w+", line):
        types.append(re.findall(r"\w+", line)[-1])
    self.types = list(set(types))

  def is_valid(self):
    return self.token and self.keywords

  def is_in_list(self, list):
    return len(set(self.keywords) & set(list)) > 0

def find_tokens():
  black_list = [
    "KW_PARSER",
    "KW_REWRITE",
    "KW_DESTINATION",
    "KW_LOG",
    "KW_OPTIONS",
    "KW_INCLUDE",
    "KW_BLOCK",
    "KW_JUNCTION",
    "KW_CHANNEL",
    "KW_IF",
    "KW_ELSE",
    "KW_ELIF"
  ]
  token_list = []
  file_list = []

  try:
    files = subprocess.check_output('find -name "*.ym"', stderr=subprocess.STDOUT, shell=True)
  except:
    print("Error in find")
    return
  file_list = files.decode().split("\n")
  file_list.append("lib/cfg-grammar.y")
  file_list = list(filter(None, file_list))

  for file_path in file_list:
    file = open(file_path)
    for line in file:
      if "%token" in line:
        token = re.findall("KW_[A-Z0-9_]+", line)
        if token and not token[0] in black_list:
          token_list.append(token[0])
  return list(set(token_list))

sources = [
  "default_network_drivers",
  "internal",
  "file", "wildcard_file",
  "linux_audit",
  "network",
  "nodejs",
  "mbox",
  "osquery",
  "pipe",
  "pacct",
  "program",
  "python", "python-fetcher",
  "snmptrap",
  "sun_streams",
  "syslog",
  "system", "systemd_journal", "systemd_syslog",
  "tcp", "tcp6", "udp", "udp6",
  "unix_stream", "unix_dgram",
  "stdin"
]

destinations = [
  "amqp",
  "elasticsearch",
  "elasticsearch2",
  "file",
  "graphite",
  "graylog2",
  "hdfs",
  "http",
  "kafka",
  "loggly",
  "logmatic",
  "mongodb",
  "network",
  "osquery",
  "pipe",
  "program",
  "pseudofile",
  "python",
  "redis",
  "riemann",
  "slack",
  "smtp",
  "splunk",
  "stomp",
  "syslog",
  "syslog-ng",
  "tcp", "tcp6", "udp", "udp6",
  "telegram",
  "unix_stream", "unix_dgram",
  "usertty"
]

filters = [
  "facility",
  "filter",
  "host",
  "in_list",
  "level", "priority",
  "match",
  "message",
  "netmask", "netmask6",
  "program",
  "source",
  "tags"
]

parsers = [
  "syslog_parser",
  "csv_parser",
  "kv_parser",
  "json_parser",
  "xml",
  "date_parser",
  "apache_accesslog_parser",
  "cisco_parser",
  "linux_audit_parser",
  "python",
  "ewmm_parser",
  "iptables_parser",
  "db_parser",
  "grouping_by",
  "add_contextual_data",
  "geoip",
  "geoip2"
]

rewrites = [
  "subst",
  "set",
  "unset",
  "groupset",
  "map_value_pairs",
  "set_tag",
  "clear_tag"
]

#todo: scl, template fo block

commands = []
for token in find_tokens():
  command = Command(token, None, None, None)
  command.get_grep_list()
  command.find_keywords()
  command.find_types()
  if command.is_valid():
    commands.append(command)

i = 0
for command in commands:
  if command.is_in_list(rewrites):
    i+=1
    print(command.token, command.keywords, command.types)
print(i)