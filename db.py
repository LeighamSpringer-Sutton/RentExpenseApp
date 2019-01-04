import sqlite3
class Db(object):
    def __init__(self,dbfile):
        self.dbfile = dbfile
        self.conn = sqlite3.connect(self.dbfile)
        self.cursor = self.conn.cursor()
        self.cursor.close()
        self.conn.close()
    def create_table(self):
        self.conn = sqlite3.connect(self.dbfile)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS CityData(city TEXT,
        Aprt_1br  INTEGER,
        Aprt_3br INTEGER,
        Description TEXT,
        Province TEXT)""")
        self.conn.commit()

    def insert_into(self,city,aprt1,aprt3,Description,Province):
        self.conn = sqlite3.connect(self.dbfile)
        self.cursor = self.conn.cursor()
        self.cursor.execute("INSERT INTO CityData VALUES (?,?,?,?,?)",(city,aprt1,aprt3,Description,Province))
        self.conn.commit()
    def get_data(self,city = None,income_to_spend = None):
        self.conn = sqlite3.connect(self.dbfile)
        self.cursor = self.conn.cursor()
        if city:
            #comma after item in brackets to signify tuple
            self.cursor.execute("SELECT * FROM CityData WHERE City = ?",(city,))
            data = self.cursor.fetchall()
            return data
        if income_to_spend:
            self.cursor.execute("SELECT * FROM CityData WHERE Aprt_1br  <=?", (income_to_spend,))
            data = self.cursor.fetchall()
            return data
        self.cursor.execute("SELECT * FROM CityData")
        data = self.cursor.fetchall()
        return data
    def alter_column(self,col):
        self.conn = sqlite3.connect(self.dbfile)
        self.cursor = self.conn.cursor()
        self.cursor.execute("ALTER TABLE CityData ADD COLUMN {}".format(col))
        self.conn.commit()
        self.close_database()
    def close_database(self):
        self.cursor.close()
        self.conn.close()
    def update(self,data,city):
        self.conn = sqlite3.connect(self.dbfile)
        self.cursor = self.conn.cursor()
        self.cursor.execute("UPDATE CityData SET Description = ? WHERE City = ?",(data,city))
        self.conn.commit()
        self.close_database()
    def delete(self,city):
        self.conn = sqlite3.connect(self.dbfile)
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM CityData WHERE City = ?",(city,))
        self.conn.commit()
        self.close_database()