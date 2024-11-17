import mysql.connector
from mysql.connector import errorcode

class mysql_sync:
    # mysql connection init
    def __init__(self,):
        pass
    def conn(self, conf):
        try:
            self.cnx = mysql.connector.connect(
                                pool_name = "local",
                                pool_size = 32,
                                **conf)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise("Database does not exist")
            else:
                raise(err)

    def execute(self, sqls="", vals=""):
        if not len(sqls):
            pass
        try:
            cursor = self.cnx.cursor()
            cursor.execute(sqls, vals)
            cursor.close()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                raise("already exists.")
            else:
                raise(err.msg)

    def execute_many(self, sqls="", vals=""):
        try:
            cursor = self.cnx.cursor()
            cursor.executemany(sqls, vals)
            cursor.close()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                raise IOError("already exists.")
            else:
                raise BaseException
