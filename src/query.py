import psycopg2
import config

def initConn():
    """Renvoie un objet connexion psycopg2"""
    return psycopg2.connect( host=config.hostname, user=config.username, password=config.password, dbname=config.database, port = config.port  )

def doQuery(conn,SQL) :
    """Renvoie le résultat de la requete SQL, conn est l'objet connexion psycopg2"""
    cur = conn.cursor()
    cur.execute(SQL)
    res = cur.fetchall()
    cur.close()
    return res

def doNoReturnQuery(conn, SQL):
    """Envoie une requete SQL qui n'attend pas forcement retour (un INSERT par exemple)"""
    cur = conn.cursor()
    cur.execute(SQL)
    conn.commit()
    res = False
    if len(conn.notices) > 0:
        res = conn.notices[-1]
    cur.close()
    if res:
        return res              #Mauvaise ecriture des triggers, renvoient des notices au lieu de renvoyer des erreurs donc oblige de gerer comme ca

    
