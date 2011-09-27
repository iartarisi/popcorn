import redis

from ConfigParser import RawConfigParser

CONFIG_FILE = '/etc/popcorn.conf'

config = RawConfigParser()
config.read(CONFIG_FILE)
rdb = redis.Redis(config.get('redis', 'hostname'),
                  int(config.get('redis', 'port')),
                  int(config.get('redis', 'db')))
