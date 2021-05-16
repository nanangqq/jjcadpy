import sqlalchemy

host = 'localhost'
port = '5432'
db_name = 'postgres'
user = 'postgres'
password = ''

con = sqlalchemy.create_engine('postgresql://%s:%s@%s:%s/%s'%(user, password, host, port, db_name))

