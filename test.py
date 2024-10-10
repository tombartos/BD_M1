import psycopg2

hostname = 'localhost'
username = 'postgres'
password = 'Tom141203' 
database = 'postgres'

#Ici votre code d’interrogation de la BDD
def doQuery(conn,SQL) :
    cur = conn.cursor()
    cur.execute(SQL)
    return cur.fetchall()


print("connection BDD ... ")
con = psycopg2.connect( host=hostname, user=username, password=password,
dbname=database )
# boucle de l’application
while(True):
    req = str(input("Requete a envoyer, (0 pour quitter) "))
    if req =="0":
        break
    print(doQuery(con, req))
        