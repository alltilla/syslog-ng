{
  "LL_CONTEXT_DESTINATION": [
    {
      "option_name": "KW_HOST",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_SMTP",
        "KW_AMQP",
        "KW_SQL",
        "KW_SNMPDEST",
        "KW_REDIS"
      ]
    },
    {
      "option_name": "KW_PATH",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB"
      ]
    },
    {
      "option_name": "KW_PORT",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_SMTP",
        "KW_AMQP",
        "KW_RIEMANN",
        "KW_SNMPDEST",
        "KW_REDIS"
      ]
    },
    {
      "option_name": "KW_SERVERS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB"
      ]
    },
    {
      "option_name": "KW_SAFE_MODE",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB"
      ]
    },
    {
      "option_name": "KW_PASSWORD",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_AMQP",
        "KW_SQL",
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_MONGODB",
      "option_value": [
        "KW_IFDEF"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB"
      ]
    },
    {
      "option_name": "KW_MONGODB",
      "option_value": [
        "KW_ENDIF"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB"
      ]
    },
    {
      "option_name": "KW_USERNAME",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_AMQP",
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_DATABASE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_COLLECTION",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB"
      ]
    },
    {
      "option_name": "KW_BATCH_TIMEOUT",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_JAVA",
        "KW_STOMP",
        "KW_PYTHON",
        "KW_SMTP",
        "KW_AMQP",
        "KW_SQL",
        "KW_HTTP",
        "KW_RIEMANN",
        "KW_REDIS"
      ]
    },
    {
      "option_name": "KW_BATCH_LINES",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_JAVA",
        "KW_STOMP",
        "KW_PYTHON",
        "KW_SMTP",
        "KW_AMQP",
        "KW_SQL",
        "KW_HTTP",
        "KW_RIEMANN",
        "KW_REDIS"
      ]
    },
    {
      "option_name": "KW_RETRIES",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_JAVA",
        "KW_STOMP",
        "KW_PYTHON",
        "KW_SMTP",
        "KW_AMQP",
        "KW_SQL",
        "KW_HTTP",
        "KW_RIEMANN",
        "KW_REDIS"
      ]
    },
    {
      "option_name": "KW_THROTTLE",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_JAVA",
        "KW_PROGRAM",
        "KW_STOMP",
        "KW_FILE",
        "KW_PIPE",
        "KW_PYTHON",
        "KW_KAFKA",
        "KW_SMTP",
        "KW_AMQP",
        "KW_SQL",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_HTTP",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM",
        "KW_RIEMANN",
        "KW_SNMPDEST",
        "KW_REDIS",
        "KW_PSEUDOFILE"
      ]
    },
    {
      "option_name": "KW_MONGODB",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB"
      ]
    },
    {
      "option_name": "KW_LOG_FIFO_SIZE",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_JAVA",
        "KW_PROGRAM",
        "KW_STOMP",
        "KW_FILE",
        "KW_PIPE",
        "KW_PYTHON",
        "KW_KAFKA",
        "KW_SMTP",
        "KW_AMQP",
        "KW_SQL",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_HTTP",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM",
        "KW_RIEMANN",
        "KW_SNMPDEST",
        "KW_REDIS",
        "KW_PSEUDOFILE"
      ]
    },
    {
      "option_name": "KW_PERSIST_NAME",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_JAVA",
        "KW_PROGRAM",
        "KW_STOMP",
        "KW_FILE",
        "KW_PIPE",
        "KW_PYTHON",
        "KW_KAFKA",
        "KW_SMTP",
        "KW_AMQP",
        "KW_SQL",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_HTTP",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM",
        "KW_RIEMANN",
        "KW_SNMPDEST",
        "KW_REDIS",
        "KW_PSEUDOFILE"
      ]
    },
    {
      "option_name": "KW_SEND_TIME_ZONE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_JAVA",
        "KW_PROGRAM",
        "KW_STOMP",
        "KW_FILE",
        "KW_PIPE",
        "KW_PYTHON",
        "KW_KAFKA",
        "KW_SMTP",
        "KW_AMQP",
        "KW_SQL",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_HTTP",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM",
        "KW_RIEMANN",
        "KW_REDIS",
        "KW_PSEUDOFILE"
      ]
    },
    {
      "option_name": "KW_TIME_ZONE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_JAVA",
        "KW_PROGRAM",
        "KW_STOMP",
        "KW_FILE",
        "KW_PIPE",
        "KW_PYTHON",
        "KW_KAFKA",
        "KW_SMTP",
        "KW_AMQP",
        "KW_SQL",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_HTTP",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM",
        "KW_RIEMANN",
        "KW_REDIS",
        "KW_PSEUDOFILE"
      ]
    },
    {
      "option_name": "KW_LOCAL_TIME_ZONE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_JAVA",
        "KW_PROGRAM",
        "KW_STOMP",
        "KW_FILE",
        "KW_PIPE",
        "KW_PYTHON",
        "KW_KAFKA",
        "KW_SMTP",
        "KW_AMQP",
        "KW_SQL",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_HTTP",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM",
        "KW_RIEMANN",
        "KW_SNMPDEST",
        "KW_REDIS",
        "KW_PSEUDOFILE"
      ]
    },
    {
      "option_name": "KW_FRAC_DIGITS",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_JAVA",
        "KW_PROGRAM",
        "KW_STOMP",
        "KW_FILE",
        "KW_PIPE",
        "KW_PYTHON",
        "KW_KAFKA",
        "KW_SMTP",
        "KW_AMQP",
        "KW_SQL",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_HTTP",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM",
        "KW_RIEMANN",
        "KW_REDIS",
        "KW_PSEUDOFILE"
      ]
    },
    {
      "option_name": "KW_TS_FORMAT",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_JAVA",
        "KW_PROGRAM",
        "KW_STOMP",
        "KW_FILE",
        "KW_PIPE",
        "KW_PYTHON",
        "KW_KAFKA",
        "KW_SMTP",
        "KW_AMQP",
        "KW_SQL",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_HTTP",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM",
        "KW_RIEMANN",
        "KW_REDIS",
        "KW_PSEUDOFILE"
      ]
    },
    {
      "option_name": "KW_ON_ERROR",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB",
        "KW_JAVA",
        "KW_PROGRAM",
        "KW_STOMP",
        "KW_FILE",
        "KW_PIPE",
        "KW_PYTHON",
        "KW_KAFKA",
        "KW_SMTP",
        "KW_AMQP",
        "KW_SQL",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_HTTP",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM",
        "KW_RIEMANN",
        "KW_REDIS",
        "KW_PSEUDOFILE"
      ]
    },
    {
      "option_name": "KW_URI",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MONGODB"
      ]
    },
    {
      "option_name": "KW_EXCLUDE",
      "option_value": [
        "string_list"
      ],
      "parent_options": [
        "KW_VALUE_PAIRS"
      ],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_PYTHON",
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_KEY",
      "option_value": [
        "string_list"
      ],
      "parent_options": [
        "KW_VALUE_PAIRS"
      ],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_PYTHON",
        "KW_AMQP"
      ]
    },
    {
      "option_name": "",
      "option_value": [
        "KW_KEY",
        "string"
      ],
      "parent_options": [
        "KW_VALUE_PAIRS"
      ],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_PYTHON",
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_SHIFT",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [
        "KW_VALUE_PAIRS",
        "KW_REKEY"
      ],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_PYTHON",
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_PAIR",
      "option_value": [
        "string",
        "template_content"
      ],
      "parent_options": [
        "KW_VALUE_PAIRS"
      ],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_PYTHON",
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_PAIR",
      "option_value": [
        "string",
        "':'",
        "template_content"
      ],
      "parent_options": [
        "KW_VALUE_PAIRS"
      ],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_PYTHON",
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_SCOPE",
      "option_value": [
        "vp_scope_list"
      ],
      "parent_options": [
        "KW_VALUE_PAIRS"
      ],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_PYTHON",
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_REPLACE_PREFIX",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_VALUE_PAIRS",
        "KW_REKEY"
      ],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_PYTHON",
        "KW_AMQP"
      ]
    },
    {
      "option_name": "",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_VALUE_PAIRS",
        "KW_REKEY"
      ],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_PYTHON",
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_ADD_PREFIX",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_VALUE_PAIRS",
        "KW_REKEY"
      ],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_PYTHON",
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_SHIFT_LEVELS",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [
        "KW_VALUE_PAIRS",
        "KW_REKEY"
      ],
      "root_driver": [
        "KW_MONGODB",
        "KW_STOMP",
        "KW_PYTHON",
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_LOADERS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON"
      ]
    },
    {
      "option_name": "KW_OPTIONS",
      "option_value": [
        "string",
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON"
      ]
    },
    {
      "option_name": "KW_CLASS",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON"
      ]
    },
    {
      "option_name": "KW_IMPORTS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON"
      ]
    },
    {
      "option_name": "KW_TEMPLATE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_JAVA",
        "KW_PROGRAM",
        "KW_FILE",
        "KW_PIPE",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_FLAGS",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_PIPE",
        "KW_SQL",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_CLASS_NAME",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_JAVA"
      ]
    },
    {
      "option_name": "KW_OPTION",
      "option_value": [
        "string",
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_JAVA"
      ]
    },
    {
      "option_name": "KW_JAVA",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_JAVA"
      ]
    },
    {
      "option_name": "KW_CLASS_PATH",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_JAVA"
      ]
    },
    {
      "option_name": "KW_MARK_FREQ",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_PIPE",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_PIPE",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_TEMPLATE_ESCAPE",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_PIPE",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_MARK_MODE",
      "option_value": [
        "KW_INTERNAL"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_PIPE",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_PAD_SIZE",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_PIPE",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_FLUSH_TIMEOUT",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_PIPE",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_SUPPRESS",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_PIPE",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_FLUSH_LINES",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_PIPE",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_MARK_MODE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_PIPE",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_KEEP_ALIVE",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_PROGRAM",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM"
      ]
    },
    {
      "option_name": "KW_INHERIT_ENVIRONMENT",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM"
      ]
    },
    {
      "option_name": "KW_TAGS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_STOMP",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_STOMP"
      ]
    },
    {
      "option_name": "KW_PERSISTENT",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_STOMP",
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_ACK",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_STOMP"
      ]
    },
    {
      "option_name": "KW_STOMP_DESTINATION",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_STOMP"
      ]
    },
    {
      "option_name": "KW_BODY",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_STOMP",
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_PYTHON",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON"
      ]
    },
    {
      "option_name": "KW_CREATE_DIRS",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE"
      ]
    },
    {
      "option_name": "KW_OVERWRITE_IF_OLDER",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE"
      ]
    },
    {
      "option_name": "KW_FSYNC",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE"
      ]
    },
    {
      "option_name": "KW_TIME_REAP",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_FILE",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE"
      ]
    },
    {
      "option_name": "KW_GROUP",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_PERM",
      "option_value": [
        "LL_NUMBER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_DIR_OWNER",
      "option_value": [
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_PERM",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_OWNER",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_DIR_GROUP",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_DIR_GROUP",
      "option_value": [
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_OWNER",
      "option_value": [
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_GROUP",
      "option_value": [
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_DIR_OWNER",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_DIR_PERM",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_DIR_PERM",
      "option_value": [
        "LL_NUMBER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_OPTIONAL",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE"
      ]
    },
    {
      "option_name": "KW_PIPE",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_TEMPLATE",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PSEUDOFILE"
      ]
    },
    {
      "option_name": "KW_PROPERTIES_FILE",
      "option_value": [
        "path_check"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_KAFKA"
      ]
    },
    {
      "option_name": "KW_CONFIG",
      "option_value": [
        "kafka_property"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_KAFKA"
      ]
    },
    {
      "option_name": "KW_BOOTSTRAP_SERVERS",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_KAFKA"
      ]
    },
    {
      "option_name": "KW_SYNC_SEND",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_KAFKA"
      ]
    },
    {
      "option_name": "KW_WORKERS",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_KAFKA",
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_FLUSH_TIMEOUT_ON_RELOAD",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_KAFKA"
      ]
    },
    {
      "option_name": "KW_POLL_TIMEOUT",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_KAFKA"
      ]
    },
    {
      "option_name": "KW_CLIENT_LIB_DIR",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_KAFKA"
      ]
    },
    {
      "option_name": "KW_FLUSH_TIMEOUT_ON_SHUTDOWN",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_KAFKA"
      ]
    },
    {
      "option_name": "KW_KAFKA",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_KAFKA"
      ]
    },
    {
      "option_name": "KW_KEY",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_KAFKA"
      ]
    },
    {
      "option_name": "KW_TOPIC",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_KAFKA"
      ]
    },
    {
      "option_name": "KW_MESSAGE",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_KAFKA"
      ]
    },
    {
      "option_name": "KW_TIMEOUT",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP",
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_TYPE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_NULL",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_COLUMNS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_TO",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SMTP"
      ]
    },
    {
      "option_name": "KW_BCC",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SMTP"
      ]
    },
    {
      "option_name": "KW_SENDER",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SMTP"
      ]
    },
    {
      "option_name": "KW_BODY",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SMTP",
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_REPLY_TO",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SMTP"
      ]
    },
    {
      "option_name": "KW_SMTP",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SMTP"
      ]
    },
    {
      "option_name": "KW_HEADER",
      "option_value": [
        "string",
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SMTP"
      ]
    },
    {
      "option_name": "KW_FROM",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SMTP"
      ]
    },
    {
      "option_name": "KW_SUBJECT",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SMTP"
      ]
    },
    {
      "option_name": "KW_CC",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SMTP"
      ]
    },
    {
      "option_name": "KW_AUTH_METHOD",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_CERT_FILE",
      "option_value": [
        "path_check"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_AMQP",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_HTTP",
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_CA_FILE",
      "option_value": [
        "path_check"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_AMQP",
        "KW_HTTP",
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_KEY_FILE",
      "option_value": [
        "path_secret"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_AMQP",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_HTTP",
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_PEER_VERIFY",
      "option_value": [
        "yesno"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_AMQP",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_EXCHANGE_DECLARE",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_MAX_CHANNEL",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_ROUTING_KEY",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_CERT_FILE",
      "option_value": [
        "path_check"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_AMQP",
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_CA_FILE",
      "option_value": [
        "path_check"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_AMQP",
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_KEY_FILE",
      "option_value": [
        "path_secret"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_AMQP",
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_PEER_VERIFY",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_AMQP",
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_FRAME_SIZE",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_EXCHANGE_TYPE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_VHOST",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_HEARTBEAT",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_EXCHANGE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_AMQP",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_AMQP"
      ]
    },
    {
      "option_name": "KW_CREATE_STATEMENT_APPEND",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_INDEXES",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_DBD_OPTION",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_DBD_OPTION",
      "option_value": [
        "string",
        "LL_NUMBER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_TABLE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_VALUES",
      "option_value": [
        "KW_DEFAULT"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_VALUES",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_PORT",
      "option_value": [
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SQL",
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_SESSION_STATEMENTS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_SQL",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_IGNORE_TNS_CONFIG",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SQL"
      ]
    },
    {
      "option_name": "KW_UNIX_DGRAM",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_SO_RCVBUF",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_SO_BROADCAST",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_SO_REUSEPORT",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_SO_SNDBUF",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_SO_KEEPALIVE",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_UNIX_STREAM",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_LOCALIP",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_IP_TOS",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TCP_KEEPALIVE_INTVL",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TCP_KEEPALIVE_TIME",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TCP_KEEPALIVE_PROBES",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_IP_FREEBIND",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_IP_TTL",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_INTERFACE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_LOCALPORT",
      "option_value": [
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TLS",
      "option_value": [
        "KW_ENDIF"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_SSL_OPTIONS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_CA_DIR",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_CIPHER_SUITE",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_PEER_VERIFY",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_PKCS12_FILE",
      "option_value": [
        "path_check"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TRUSTED_DN",
      "option_value": [
        "string_list"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_ECDH_CURVE_LIST",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_ALLOW_COMPRESS",
      "option_value": [
        "yesno"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_DHPARAM_FILE",
      "option_value": [
        "path_check"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_CRL_DIR",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TLS",
      "option_value": [
        "KW_IFDEF"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TRUSTED_KEYS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_IP_PROTOCOL",
      "option_value": [
        "LL_NUMBER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TRANSPORT",
      "option_value": [
        "KW_TLS"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TRANSPORT",
      "option_value": [
        "KW_TCP"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TRANSPORT",
      "option_value": [
        "KW_UDP"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TRANSPORT",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_SPOOF_SOURCE_MAX_MSGLEN",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6"
      ]
    },
    {
      "option_name": "KW_UDP",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP"
      ]
    },
    {
      "option_name": "KW_SERVERS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [
        "KW_FAILOVER"
      ],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TCP_PROBE_INTERVAL",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [
        "KW_FAILOVER",
        "KW_FAILBACK"
      ],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_DESTPORT",
      "option_value": [
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_FAILOVER_SERVERS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_CLOSE_ON_INPUT",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UNIX_STREAM",
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_SPOOF_SOURCE",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP",
        "KW_UDP6",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_UDP6",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP6"
      ]
    },
    {
      "option_name": "KW_TCP6",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_TCP6"
      ]
    },
    {
      "option_name": "KW_SNI",
      "option_value": [
        "yesno"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_TCP6",
        "KW_TCP",
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TCP",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_NETWORK",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK"
      ]
    },
    {
      "option_name": "KW_SYSLOG",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_METHOD",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_USE_SYSTEM_CERT_STORE",
      "option_value": [
        "yesno"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_SSL_VERSION",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_HTTP",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_HEADERS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_BODY_SUFFIX",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_AUTH_HEADER",
      "option_value": [
        "http_auth_header_plugin"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_USER_AGENT",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_USER",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_ACCEPT_REDIRECTS",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_BODY_PREFIX",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_CIPHER_SUITE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_CA_DIR",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_USE_SYSTEM_CERT_STORE",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_SSL_VERSION",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_URL",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_BATCH_BYTES",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_DELIMITER",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_HTTP"
      ]
    },
    {
      "option_name": "KW_HOST",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_SERVER",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_SERVICE",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_EVENT_TIME",
      "option_value": [
        "template_content",
        "KW_MICROSECONDS"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_EVENT_TIME",
      "option_value": [
        "template_content",
        "KW_SECONDS"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_DESCRIPTION",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_STATE",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_TTL",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_ATTRIBUTES",
      "option_value": [
        "attribute_option"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_KEY",
      "option_value": [
        "path_secret"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_METRIC",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_RIEMANN",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_CA_FILE",
      "option_value": [
        "path_check"
      ],
      "parent_options": [
        "KW_TYPE"
      ],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_TYPE"
      ],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_KEY_FILE",
      "option_value": [
        "path_secret"
      ],
      "parent_options": [
        "KW_TYPE"
      ],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_KEY",
      "option_value": [
        "path_secret"
      ],
      "parent_options": [
        "KW_TYPE"
      ],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_CERT_FILE",
      "option_value": [
        "path_check"
      ],
      "parent_options": [
        "KW_TYPE"
      ],
      "root_driver": [
        "KW_RIEMANN"
      ]
    },
    {
      "option_name": "KW_TRAP_OBJ",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SNMPDEST"
      ]
    },
    {
      "option_name": "KW_ENC_ALGORITHM",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SNMPDEST"
      ]
    },
    {
      "option_name": "KW_VERSION",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SNMPDEST"
      ]
    },
    {
      "option_name": "KW_ENC_PASSWORD",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SNMPDEST"
      ]
    },
    {
      "option_name": "KW_SNMP_OBJ",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SNMPDEST"
      ]
    },
    {
      "option_name": "KW_AUTH_PASSWORD",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SNMPDEST"
      ]
    },
    {
      "option_name": "KW_AUTH_ALGORITHM",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SNMPDEST"
      ]
    },
    {
      "option_name": "KW_AUTH_USERNAME",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SNMPDEST"
      ]
    },
    {
      "option_name": "KW_SNMPDEST",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SNMPDEST"
      ]
    },
    {
      "option_name": "KW_COMMUNITY",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SNMPDEST"
      ]
    },
    {
      "option_name": "KW_ENGINE_ID",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SNMPDEST"
      ]
    },
    {
      "option_name": "KW_USERTTY",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_USERTTY"
      ]
    },
    {
      "option_name": "KW_AUTH",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_REDIS"
      ]
    },
    {
      "option_name": "KW_COMMAND",
      "option_value": [
        "string",
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_REDIS"
      ]
    },
    {
      "option_name": "KW_REDIS",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_REDIS"
      ]
    },
    {
      "option_name": "KW_PSEUDOFILE",
      "option_value": [
        "path_check",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PSEUDOFILE"
      ]
    }
  ],
  "LL_CONTEXT_PARSER": [
    {
      "option_name": "KW_TIME_ZONE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SYSLOG_PARSER",
        "KW_DATE_PARSER"
      ]
    },
    {
      "option_name": "KW_TIME_STAMP",
      "option_value": [
        "date_parser_stamp"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_DATE_PARSER"
      ]
    },
    {
      "option_name": "KW_LOADERS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON"
      ]
    },
    {
      "option_name": "KW_OPTIONS",
      "option_value": [
        "string",
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON"
      ]
    },
    {
      "option_name": "KW_CLASS",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON"
      ]
    },
    {
      "option_name": "KW_IMPORTS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON"
      ]
    },
    {
      "option_name": "KW_DEFAULT_LEVEL",
      "option_value": [
        "level_string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SYSLOG_PARSER"
      ]
    },
    {
      "option_name": "KW_DEFAULT_FACILITY",
      "option_value": [
        "facility_string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SYSLOG_PARSER"
      ]
    },
    {
      "option_name": "KW_TEMPLATE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SYSLOG_PARSER",
        "KW_JSON_PARSER",
        "KW_DATE_PARSER",
        "KW_SNMPTRAPD_PARSER",
        "KW_TAGS_PARSER",
        "KW_XML",
        "KW_GROUPING_BY",
        "KW_DB_PARSER",
        "KW_CSV_PARSER",
        "KW_LINUX_AUDIT_PARSER",
        "KW_KV_PARSER"
      ]
    },
    {
      "option_name": "KW_FLAGS",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SYSLOG_PARSER"
      ]
    },
    {
      "option_name": "KW_FLAGS",
      "option_value": [
        "KW_CHECK_HOSTNAME"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SYSLOG_PARSER"
      ]
    },
    {
      "option_name": "KW_OPTION",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "LL_IDENTIFIER"
      ]
    },
    {
      "option_name": "KW_PREFIX",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_JSON_PARSER",
        "KW_GEOIP2",
        "KW_ADD_CONTEXTUAL_DATA",
        "KW_SNMPTRAPD_PARSER",
        "KW_XML",
        "KW_CSV_PARSER",
        "KW_LINUX_AUDIT_PARSER",
        "KW_KV_PARSER"
      ]
    },
    {
      "option_name": "KW_MARKER",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_JSON_PARSER"
      ]
    },
    {
      "option_name": "KW_EXTRACT_PREFIX",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_JSON_PARSER"
      ]
    },
    {
      "option_name": "",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_GEOIP2"
      ]
    },
    {
      "option_name": "KW_DATABASE",
      "option_value": [
        "path_check"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_GEOIP2"
      ]
    },
    {
      "option_name": "KW_DATABASE",
      "option_value": [
        "path_no_check"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_ADD_CONTEXTUAL_DATA"
      ]
    },
    {
      "option_name": "KW_IGNORE_CASE",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_ADD_CONTEXTUAL_DATA"
      ]
    },
    {
      "option_name": "KW_DEFAULT_SELECTOR",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_ADD_CONTEXTUAL_DATA"
      ]
    },
    {
      "option_name": "KW_SELECTOR",
      "option_value": [
        "LL_STRING"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_ADD_CONTEXTUAL_DATA"
      ]
    },
    {
      "option_name": "KW_FILTERS",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_SELECTOR"
      ],
      "root_driver": [
        "KW_ADD_CONTEXTUAL_DATA"
      ]
    },
    {
      "option_name": "KW_FLAGS",
      "option_value": [
        "date_parser_flags"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_DATE_PARSER"
      ]
    },
    {
      "option_name": "KW_FORMAT",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_DATE_PARSER"
      ]
    },
    {
      "option_name": "KW_EXCLUDE",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MAP_VALUE_PAIRS"
      ]
    },
    {
      "option_name": "KW_KEY",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MAP_VALUE_PAIRS"
      ]
    },
    {
      "option_name": "",
      "option_value": [
        "KW_KEY",
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MAP_VALUE_PAIRS"
      ]
    },
    {
      "option_name": "KW_SHIFT",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [
        "KW_REKEY"
      ],
      "root_driver": [
        "KW_MAP_VALUE_PAIRS"
      ]
    },
    {
      "option_name": "KW_PAIR",
      "option_value": [
        "string",
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MAP_VALUE_PAIRS"
      ]
    },
    {
      "option_name": "KW_PAIR",
      "option_value": [
        "string",
        "':'",
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MAP_VALUE_PAIRS"
      ]
    },
    {
      "option_name": "KW_SCOPE",
      "option_value": [
        "vp_scope_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MAP_VALUE_PAIRS"
      ]
    },
    {
      "option_name": "KW_REPLACE_PREFIX",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_REKEY"
      ],
      "root_driver": [
        "KW_MAP_VALUE_PAIRS"
      ]
    },
    {
      "option_name": "",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_REKEY"
      ],
      "root_driver": [
        "KW_MAP_VALUE_PAIRS"
      ]
    },
    {
      "option_name": "KW_ADD_PREFIX",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_REKEY"
      ],
      "root_driver": [
        "KW_MAP_VALUE_PAIRS"
      ]
    },
    {
      "option_name": "KW_SHIFT_LEVELS",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [
        "KW_REKEY"
      ],
      "root_driver": [
        "KW_MAP_VALUE_PAIRS"
      ]
    },
    {
      "option_name": "KW_SET_MESSAGE_MACRO",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SNMPTRAPD_PARSER"
      ]
    },
    {
      "option_name": "KW_CREATE_LISTS",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_XML"
      ]
    },
    {
      "option_name": "KW_STRIP_WHITESPACES",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_XML"
      ]
    },
    {
      "option_name": "KW_EXCLUDE_TAGS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_XML"
      ]
    },
    {
      "option_name": "KW_DROP_INVALID",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_XML"
      ]
    },
    {
      "option_name": "KW_KEY",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_GROUPING_BY"
      ]
    },
    {
      "option_name": "KW_INJECT_MODE",
      "option_value": [
        "stateful_parser_inject_mode"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_GROUPING_BY",
        "KW_DB_PARSER"
      ]
    },
    {
      "option_name": "KW_TIMEOUT",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_GROUPING_BY"
      ]
    },
    {
      "option_name": "KW_AGGREGATE",
      "option_value": [
        "synthetic_message"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_GROUPING_BY"
      ]
    },
    {
      "option_name": "KW_WHERE",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_GROUPING_BY"
      ]
    },
    {
      "option_name": "KW_SCOPE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_GROUPING_BY"
      ]
    },
    {
      "option_name": "KW_SORT_KEY",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_GROUPING_BY"
      ]
    },
    {
      "option_name": "KW_HAVING",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_GROUPING_BY"
      ]
    },
    {
      "option_name": "KW_TRIGGER",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_GROUPING_BY"
      ]
    },
    {
      "option_name": "KW_PROGRAM_TEMPLATE",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_DB_PARSER"
      ]
    },
    {
      "option_name": "KW_DROP_UNMATCHED",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_DB_PARSER"
      ]
    },
    {
      "option_name": "KW_MESSAGE_TEMPLATE",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_DB_PARSER"
      ]
    },
    {
      "option_name": "KW_FILE",
      "option_value": [
        "path_no_check"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_DB_PARSER"
      ]
    },
    {
      "option_name": "KW_NULL",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_CSV_PARSER"
      ]
    },
    {
      "option_name": "KW_QUOTES",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_CSV_PARSER"
      ]
    },
    {
      "option_name": "KW_DIALECT",
      "option_value": [
        "parser_csv_dialect"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_CSV_PARSER"
      ]
    },
    {
      "option_name": "KW_FLAGS",
      "option_value": [
        "parser_csv_flags"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_CSV_PARSER"
      ]
    },
    {
      "option_name": "KW_COLUMNS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_CSV_PARSER"
      ]
    },
    {
      "option_name": "KW_DELIMITERS",
      "option_value": [
        "parser_csv_delimiters"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_CSV_PARSER"
      ]
    },
    {
      "option_name": "KW_QUOTE_PAIRS",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_CSV_PARSER"
      ]
    },
    {
      "option_name": "KW_PAIR_SEPARATOR",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_LINUX_AUDIT_PARSER",
        "KW_KV_PARSER"
      ]
    },
    {
      "option_name": "KW_EXTRACT_STRAY_WORDS_INTO",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_LINUX_AUDIT_PARSER",
        "KW_KV_PARSER"
      ]
    },
    {
      "option_name": "KW_VALUE_SEPARATOR",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_LINUX_AUDIT_PARSER",
        "KW_KV_PARSER"
      ]
    },
    {
      "option_name": "KW_ALLOW_PAIR_SEPARATOR_OPTION",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_LINUX_AUDIT_PARSER",
        "KW_KV_PARSER"
      ]
    }
  ],
  "LL_CONTEXT_REWRITE": [
    {
      "option_name": "KW_CONDITION",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_FIX_TIME_ZONE",
        "KW_GUESS_TIME_ZONE",
        "KW_SET_TIME_ZONE"
      ]
    },
    {
      "option_name": "",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FIX_TIME_ZONE",
        "KW_SET_TIME_ZONE"
      ]
    },
    {
      "option_name": "KW_TIME_STAMP",
      "option_value": [
        "date_parser_stamp"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FIX_TIME_ZONE",
        "KW_GUESS_TIME_ZONE",
        "KW_SET_TIME_ZONE"
      ]
    }
  ],
  "LL_CONTEXT_SOURCE": [
    {
      "option_name": "KW_PERSIST_NAME",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_OPENBSD",
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_SUN_STREAMS",
        "KW_MSG_GENERATOR",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_TIME_ZONE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_LOADERS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_PYTHON"
      ]
    },
    {
      "option_name": "KW_OPTIONS",
      "option_value": [
        "string",
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_PYTHON"
      ]
    },
    {
      "option_name": "KW_CLASS",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_PYTHON"
      ]
    },
    {
      "option_name": "KW_DEFAULT_LEVEL",
      "option_value": [
        "level_string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_DEFAULT_FACILITY",
      "option_value": [
        "facility_string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_FLAGS",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_PYTHON",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_FLAGS",
      "option_value": [
        "KW_CHECK_HOSTNAME"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_PREFIX",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SYSTEMD_JOURNAL"
      ]
    },
    {
      "option_name": "",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SUN_STREAMS",
        "KW_PROGRAM",
        "KW_FILE",
        "KW_PIPE",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_PAD_SIZE",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN"
      ]
    },
    {
      "option_name": "KW_KEEP_ALIVE",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_PROGRAM",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM"
      ]
    },
    {
      "option_name": "KW_INHERIT_ENVIRONMENT",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM"
      ]
    },
    {
      "option_name": "KW_OPENBSD",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_OPENBSD"
      ]
    },
    {
      "option_name": "KW_FORMAT",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_PYTHON",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_PYTHON_FETCHER",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER"
      ]
    },
    {
      "option_name": "KW_LOG_PREFIX",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_MSG_GENERATOR",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_TAGS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_MSG_GENERATOR",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_KEEP_HOSTNAME",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_MSG_GENERATOR",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_READ_OLD_RECORDS",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_MSG_GENERATOR",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_CHAIN_HOSTNAMES",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_MSG_GENERATOR",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_USE_DNS",
      "option_value": [
        "dnsmode"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_MSG_GENERATOR",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_DNS_CACHE",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_MSG_GENERATOR",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_USE_FQDN",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_MSG_GENERATOR",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_NORMALIZE_HOSTNAMES",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_MSG_GENERATOR",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_LOG_IW_SIZE",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_MSG_GENERATOR",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_HOST_OVERRIDE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_MSG_GENERATOR",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_PROGRAM_OVERRIDE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_MSG_GENERATOR",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_KEEP_TIMESTAMP",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_SYSTEMD_JOURNAL",
        "KW_PYTHON",
        "KW_MSG_GENERATOR",
        "KW_PROGRAM",
        "KW_RANDOM_GENERATOR",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_FETCH_NO_DATA_DELAY",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON_FETCHER",
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_SYSTEMD_JOURNAL",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SYSTEMD_JOURNAL"
      ]
    },
    {
      "option_name": "KW_LOG_FETCH_LIMIT",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SYSTEMD_JOURNAL",
        "KW_PROGRAM",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_MAX_FIELD_SIZE",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SYSTEMD_JOURNAL"
      ]
    },
    {
      "option_name": "KW_PYTHON",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PYTHON"
      ]
    },
    {
      "option_name": "KW_DOOR",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SUN_STREAMS"
      ]
    },
    {
      "option_name": "KW_SUN_STREAMS",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SUN_STREAMS"
      ]
    },
    {
      "option_name": "KW_CREATE_DIRS",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_FILE",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE"
      ]
    },
    {
      "option_name": "KW_GROUP",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_PERM",
      "option_value": [
        "LL_NUMBER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_DIR_OWNER",
      "option_value": [
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_PERM",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_OWNER",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_DIR_GROUP",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_DIR_GROUP",
      "option_value": [
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_OWNER",
      "option_value": [
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_GROUP",
      "option_value": [
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_DIR_OWNER",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_DIR_PERM",
      "option_value": [],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_DIR_PERM",
      "option_value": [
        "LL_NUMBER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_OPTIONAL",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PIPE",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_PIPE",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PIPE"
      ]
    },
    {
      "option_name": "KW_MSG_GENERATOR",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MSG_GENERATOR"
      ]
    },
    {
      "option_name": "KW_FREQ",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MSG_GENERATOR",
        "KW_RANDOM_GENERATOR"
      ]
    },
    {
      "option_name": "KW_NUM",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MSG_GENERATOR"
      ]
    },
    {
      "option_name": "KW_TEMPLATE",
      "option_value": [
        "template_content"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MSG_GENERATOR"
      ]
    },
    {
      "option_name": "KW_FREQ",
      "option_value": [
        "LL_FLOAT"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_MSG_GENERATOR",
        "KW_RANDOM_GENERATOR"
      ]
    },
    {
      "option_name": "KW_ENCODING",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_LOG_MSG_SIZE",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_TRIM_LARGE_MESSAGES",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_CHECK_HOSTNAME",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_PROGRAM",
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN",
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_TYPE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RANDOM_GENERATOR"
      ]
    },
    {
      "option_name": "KW_BYTES",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RANDOM_GENERATOR"
      ]
    },
    {
      "option_name": "KW_RANDOM_GENERATOR",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_RANDOM_GENERATOR"
      ]
    },
    {
      "option_name": "KW_RECURSIVE",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_STDIN"
      ]
    },
    {
      "option_name": "KW_FORCE_DIRECTORY_POLLING",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_STDIN"
      ]
    },
    {
      "option_name": "KW_FOLLOW_FREQ",
      "option_value": [
        "LL_FLOAT"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_STDIN"
      ]
    },
    {
      "option_name": "KW_MULTI_LINE_GARBAGE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN"
      ]
    },
    {
      "option_name": "KW_MULTI_LINE_MODE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN"
      ]
    },
    {
      "option_name": "KW_MULTI_LINE_PREFIX",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_PIPE",
        "KW_STDIN"
      ]
    },
    {
      "option_name": "KW_FOLLOW_FREQ",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_FILE",
        "KW_WILDCARD_FILE",
        "KW_STDIN"
      ]
    },
    {
      "option_name": "KW_MONITOR_METHOD",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_WILDCARD_FILE"
      ]
    },
    {
      "option_name": "KW_FILENAME_PATTERN",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_WILDCARD_FILE"
      ]
    },
    {
      "option_name": "KW_WILDCARD_FILE",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_WILDCARD_FILE"
      ]
    },
    {
      "option_name": "KW_BASE_DIR",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_WILDCARD_FILE"
      ]
    },
    {
      "option_name": "KW_MAX_FILES",
      "option_value": [
        "LL_NUMBER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_WILDCARD_FILE"
      ]
    },
    {
      "option_name": "KW_STDIN",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_STDIN"
      ]
    },
    {
      "option_name": "KW_CERT_FILE",
      "option_value": [
        "path_check"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_KEY_FILE",
      "option_value": [
        "path_secret"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_PEER_VERIFY",
      "option_value": [
        "yesno"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_PORT",
      "option_value": [
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_MAX_CONNECTIONS",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_LISTEN_BACKLOG",
      "option_value": [
        "positive_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_DYNAMIC_WINDOW_SIZE",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_DYNAMIC_WINDOW_STATS_FREQ",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_DYNAMIC_WINDOW_STATS_FREQ",
      "option_value": [
        "LL_FLOAT"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_DYNAMIC_WINDOW_REALLOC_TICKS",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_PASS_UNIX_CREDENTIALS",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_UNIX_DGRAM",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM"
      ]
    },
    {
      "option_name": "KW_SO_RCVBUF",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_SO_BROADCAST",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_SO_REUSEPORT",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_SO_SNDBUF",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_SO_KEEPALIVE",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_DGRAM",
        "KW_UNIX_STREAM",
        "KW_NETWORK",
        "KW_SYSTEMD_SYSLOG",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_UNIX_STREAM",
      "option_value": [
        "string",
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UNIX_STREAM"
      ]
    },
    {
      "option_name": "KW_LOCALIP",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_IP_TOS",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_TCP_KEEPALIVE_INTVL",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_TCP_KEEPALIVE_TIME",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_TCP_KEEPALIVE_PROBES",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_IP_FREEBIND",
      "option_value": [
        "yesno"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_IP_TTL",
      "option_value": [
        "nonnegative_integer"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_INTERFACE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_LOCALPORT",
      "option_value": [
        "string_or_number"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_NETWORK",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK"
      ]
    },
    {
      "option_name": "KW_IP",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_UDP",
        "KW_TCP6",
        "KW_UDP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_TLS",
      "option_value": [
        "KW_ENDIF"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_SSL_OPTIONS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_CA_DIR",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_CIPHER_SUITE",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_PEER_VERIFY",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_PKCS12_FILE",
      "option_value": [
        "path_check"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_TRUSTED_DN",
      "option_value": [
        "string_list"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_ECDH_CURVE_LIST",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_ALLOW_COMPRESS",
      "option_value": [
        "yesno"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_DHPARAM_FILE",
      "option_value": [
        "path_check"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_CRL_DIR",
      "option_value": [
        "string"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_TLS",
      "option_value": [
        "KW_IFDEF"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_TRUSTED_KEYS",
      "option_value": [
        "string_list"
      ],
      "parent_options": [
        "KW_TLS"
      ],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG",
        "KW_TCP6",
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_IP_PROTOCOL",
      "option_value": [
        "LL_NUMBER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TRANSPORT",
      "option_value": [
        "KW_TLS"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TRANSPORT",
      "option_value": [
        "KW_TCP"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TRANSPORT",
      "option_value": [
        "KW_UDP"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_TRANSPORT",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_NETWORK",
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_SYSTEMD_SYSLOG",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SYSTEMD_SYSLOG"
      ]
    },
    {
      "option_name": "KW_SYSLOG",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_SYSLOG"
      ]
    },
    {
      "option_name": "KW_UDP",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP"
      ]
    },
    {
      "option_name": "KW_TCP6",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_TCP6"
      ]
    },
    {
      "option_name": "KW_UDP6",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_UDP6"
      ]
    },
    {
      "option_name": "KW_TCP",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_TCP"
      ]
    },
    {
      "option_name": "KW_FILE",
      "option_value": [
        "string"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_DISKQ_SOURCE"
      ]
    },
    {
      "option_name": "KW_DISKQ_SOURCE",
      "option_value": [
        "LL_IDENTIFIER"
      ],
      "parent_options": [],
      "root_driver": [
        "KW_DISKQ_SOURCE"
      ]
    }
  ]
}
