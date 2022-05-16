import pandas as pd
import mysql.connector
from mysql.connector import Error
import logging
import sshtunnel
#from sshtunnel import open_tunnel
from sshtunnel import SSHTunnelForwarder


class SecureConection():
    
    def __init__(self):
        #Configure your credencials
        self.sshHost = "10.10.0.251"
        self.sshUsername = "ruizdev7"
        self.sshPassword = "C9p5au8naa*"
        self.databaseUsername = "dba"
        self.databasePassword = "C9p5au8naa*"
        self.dataBaseName = "MJFreeway_pro"
        self.localHost = "127.0.0.1"


    def openSSHTunnel(self,verbose=True):
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
                self.sshHost, 22,
                ssh_username = self.sshUsername,
                ssh_password = self.sshPassword,
                remote_bind_address=(self.localHost, 3306)
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

    def mysqlConnect(self):
        """Connect to a MySQL server using the SSH tunnel connection
        :return connection: Global MySQL database connection
        """

        global cnx

        try:
            cnx = mysql.connector.connect(
                host = self.localHost,
                user = self.databaseUsername,
                password = self.databasePassword,
                db = self.dataBaseName,
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
            
            
    def getCatalog(self):
        try:
            if cnx.is_connected():
                cursor = cnx.cursor()
                sql = "SELECT id, idProduct, nameProduct FROM tblCatalog"
                cursor.execute(sql)
                query = cursor.fetchall()                
                for row in query:
                    print(row)
        except Error as ex:
                print("Error during conexion: ", ex)
        
    
    def mysqldisconnect(self):
        try:
            cnx = mysql.connector.connect(
                host = self.localHost,
                user = self.databaseUsername,
                password = self.databasePassword,
                db = self.dataBaseName,
                port = server.local_bind_port
            )
            if cnx.is_connected():
                cnx.close()
                print("connection terminated: ", cnx)
        except Error as ex:
                print("Error during conexion: ", ex)

    #Disconnect and close the tunnel    
    def closeSSHTunnel(self):
        """Closes the SSH tunnel connection.
        """
        server.stop()
        print("The connection using sshtunnel has ended")