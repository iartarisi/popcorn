DB_ENGINE = 'postgresql://popcorn:popcorn@localhost/popcorn'
SUBMISSION_INTERVAL = 30

#configuration settings for mail during traceback
SMTP_SERVER=''
SMTP_PORT=25
HOST_EMAIL=''
HOST_PASS=''
ADMIN_MAIL=''

MESSAGE='From: '+HOST_EMAIL+'\n'+'To: '+ADMIN_MAIL+'\n'+'Subject: Traceback'+'\n\n'
