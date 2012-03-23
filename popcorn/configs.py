import json

with open('/home/dotcloud/environment.json', 'r') as f:
  conf = json.load(f)
DB_ENGINE = 'postgresql://popcorn:popcorn@%(host)s:%(port)s/popcorn' % {
  'host': conf['DOTCLOUD_DB_SQL_HOST'],
  'port': conf['DOTCLOUD_DB_SQL_PORT']}
SUBMISSION_INTERVAL = 30
