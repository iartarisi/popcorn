DB_ENGINE = 'postgresql://popcorn:popcorn@localhost/popcorn'
SUBMISSION_INTERVAL = 30

#configuration settings for mail during traceback
SMTP_SERVER='smtp.gmail.com'
SMTP_PORT=25
HOST_EMAIL='gauravsood.91@gmail.com'
HOST_PASS='ucertainlywontexpectthis'
ADMIN_MAIL='gauravs@sitpune.edu.in'

MESSAGE='From: '+HOST_EMAIL+'\n'+'To: '+ADMIN_MAIL+'\n'+'Subject: Traceback'+'\n\n'
