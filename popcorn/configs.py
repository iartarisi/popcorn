import redis

from ConfigParser import RawConfigParser

CONFIG_FILE = '/etc/popcorn.conf'

_config = RawConfigParser()
_config.read(CONFIG_FILE)
rdb = redis.Redis(_config.get('redis', 'hostname'),
                  int(_config.get('redis', 'port')),
                  int(_config.get('redis', 'db')))
