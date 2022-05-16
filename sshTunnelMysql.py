from sqlite3 import Cursor
import pandas as pd
import mysql.connector
from mysql.connector import Error
import logging
import sshtunnel
#from sshtunnel import open_tunnel
from sshtunnel import SSHTunnelForwarder


#Configure your credencials
sshHost = "10.10.0.251"
sshUsername = "ruizdev7"
sshPassword = "C9p5au8naa*"
databaseUsername = "dba"
databasePassword = "C9p5au8naa*"
dataBaseName = "MJFreeway_pro"
localHost = "127.0.0.1"


def openSSHTunnel(verbose=False):
    """Open an SSH tunnel and connect using a username and password.
    
    :param verbose: Set to True to show logging
    :return tunnel: Global SSH tunnel connection
    

    Args:
        verbose (bool, optional): _description_. Defaults to False.
    """
    
    if verbose:
        sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
        
    global server
    
    try:
        server = SSHTunnelForwarder(
            sshHost, 22,
            ssh_username = sshUsername,
            ssh_password = sshPassword,
            remote_bind_address=(localHost, 3306)
        )
    except Exception as e:
        print("something was wrong: {error}".format(error=e))
        server.stop()
        exit()
    
    server.start()

    print("This is port randomly assigned by sshtunnel module: ", server.local_bind_port)  
    # show assigned local port
    # work with `SECRET SERVICE` through `server.local_bind_port`.

    #server.stop()
    
def mysqlConnect():
    """Connect to a MySQL server using the SSH tunnel connection
    :return connection: Global MySQL database connection
    """
    
    global cnx
    
    try:
        cnx = mysql.connector.connect(
            host = localHost,
            user = databaseUsername,
            password = databasePassword,
            db = dataBaseName,
            port = server.local_bind_port
        )
        print("Successful conexion: ", cnx)
        cursor = cnx.cursor()
        cursor.execute("SHOW DATABASES;")
        query = cursor.fetchall()        
        for row in query:
            print("BD Available: ", row)
        infoServer = cnx.get_server_info()
        print("Information of server conexion", infoServer)
        return (cnx)
    except Error as ex:
        print("Error during conexion: ", ex)
        
        
def mysqldisconnect():
    try:
        cnx = mysql.connector.connect(
            host = localHost,
            user = databaseUsername,
            password = databasePassword,
            db = dataBaseName,
            port = server.local_bind_port
        )
        if cnx.is_connected():
            cnx.close()
            print("connection terminated: ", cnx)
    except Error as ex:
            print("Error during conexion: ", ex)

#Disconnect and close the tunnel    
def closeSSHTunnel():
    """Closes the SSH tunnel connection.
    """
    server.stop()
    print("The connection using sshtunnel has ended")

            
openSSHTunnel()
mysqlConnect()
mysqldisconnect()
closeSSHTunnel()