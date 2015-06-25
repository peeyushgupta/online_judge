from django.db.backends.signals import connection_created

def connection_setup(**kwargs):
    conn = kwargs['connection']
    with conn.cursor() as cursor:
        cursor.execute("SET character_set_results = 'latin1'")
        cursor.close()
from django.db import connection

with connection.cursor() as c:
    # I expect variable to be 'latin1'
    c.execute("show variables like 'character_set_results%'")
    c.fetchone() # returns ('character_set_results', 'utf8')

    # here I try to set it manually
    c.execute("SET character_set_results = 'latin1'")
    c.execute("show variables like 'character_set_results%'")
    c.fetchone() // returns ('character_set_results', 'latin1') #`// now it's OK


