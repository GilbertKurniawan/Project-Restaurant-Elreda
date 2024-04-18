from elreda_v1.dtos import OrderDTO

from kink import inject
from abc import ABCMeta, abstractmethod
import sqlite3
from sqlite3 import Error


@inject
class IElredaDB(metaclass=ABCMeta):
    @abstractmethod
    def find_data_by_date(self, _date):
        pass

    @abstractmethod
    def insert_all_menu_to_database_with_new_date_default_nul(self, _date):
        pass

    @abstractmethod
    def insert__into_the_total_food_menu_that_date(self, id_date, food, amt_food, drink, amt_drink):
        pass

    @abstractmethod
    def get_id_date_by_date(self, _date):
        pass

    @abstractmethod
    def get_all_data_to_report_tab(self):
        pass


@inject
class ElredaDB:
    def __init__(self, dburl=None):
        self.conn = self.create_connection(dburl)
        if self.conn is not None:
            self.c = self.conn.cursor()

    def init(self):
        pass

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    def find_data_by_date(self, _date):
        get_id_tanggal = """
        SELECT Pesanan.ID_tanggal
        FROM Pesanan
        WHERE (((Pesanan.Tanggal)=?));
        """
        self.c.execute(get_id_tanggal, (_date,))
        rows = self.c.fetchall()
        if rows == []:
            return False
        else:
            return True

    def insert_all_menu_new_date_default_nul(self, _date):
        # make unique_id
        get_all_id_tanggal = """
        SELECT Pesanan.ID_tanggal
        FROM Pesanan;
        """
        self.c.execute(get_all_id_tanggal)
        rows = self.c.fetchall()
        unique_id = "P00" + str(len(rows) + 1)

        self.c.execute('BEGIN TRANSACTION;')
        insert_date = """ insert into Pesanan (ID_tanggal, Tanggal) values (?, ?); """
        insert_all_menu_1 = """ insert into Detail_Pesanan (ID_tanggal, Menu_makanan, Jumlah_makanan, Menu_minuman, Jumlah_minuman) values (?, "Kubideh Rice", 0, "Ayran", 0 );"""
        insert_all_menu_2 = """ insert into Detail_Pesanan (ID_tanggal, Menu_makanan, Jumlah_makanan, Menu_minuman, Jumlah_minuman) values (?, "Fischteller", 0, "Coca cola", 0 );"""
        insert_all_menu_3 = """ insert into Detail_Pesanan (ID_tanggal, Menu_makanan, Jumlah_makanan, Menu_minuman, Jumlah_minuman) values (?, "Chicken Rice", 0, "Mineral Water", 0 );"""
        insert_all_menu_4 = """ insert into Detail_Pesanan (ID_tanggal, Menu_makanan, Jumlah_makanan, Menu_minuman, Jumlah_minuman) values (?, "Gemischter Salad", 0, "Tea", 0);"""
        insert_all_menu_5 = """ insert into Detail_Pesanan (ID_tanggal, Menu_makanan, Jumlah_makanan, Menu_minuman, Jumlah_minuman) values (?, "Djujeh", 0, "Coffee", 0 );"""

        self.c.execute(insert_date, (unique_id, _date))
        self.c.execute(insert_all_menu_1, (unique_id,))
        self.c.execute(insert_all_menu_2, (unique_id,))
        self.c.execute(insert_all_menu_3, (unique_id,))
        self.c.execute(insert_all_menu_4, (unique_id,))
        self.c.execute(insert_all_menu_5, (unique_id,))
        self.conn.commit()

    def insert__into_the_total_food_menu_that_date(self, id_date, food, amt_food, drink, amt_drink):
        # cari data jumlahnya total,
        # lalu jumlahkan dg penambahannya, kemudian update database

        get_total_food = """
        SELECT Detail_Pesanan.Jumlah_makanan
        FROM Detail_Pesanan
        WHERE (((Detail_Pesanan.ID_tanggal)=?) AND ((Detail_Pesanan.Menu_makanan)=?));
        """

        self.c.execute(get_total_food, (id_date, food))
        jumlah_makanan = self.c.fetchall()
        new_jumlah_makanan = int(jumlah_makanan[0][0]) + int(amt_food)

        get_total_drink = """
            SELECT Detail_Pesanan.Jumlah_minuman
            FROM Detail_Pesanan
            WHERE (((Detail_Pesanan.ID_tanggal)=?) AND ((Detail_Pesanan.Menu_minuman)=?));
            """
        self.c.execute(get_total_drink, (id_date, drink))
        jumlah_minuman = self.c.fetchall()
        new_jumlah_minuman = int(jumlah_minuman[0][0]) + int(amt_drink)

        self.c.execute('BEGIN TRANSACTION;')

        update_jumlah_makanan = """
        Update Detail_Pesanan set Jumlah_makanan=? where id_tanggal=? AND Menu_makanan=?;
        """
        update_jumlah_minuman = """
        Update Detail_Pesanan set Jumlah_minuman=? where id_tanggal=? AND Menu_minuman=?;
        """
        self.c.execute(update_jumlah_makanan, (str(new_jumlah_makanan), id_date, food))
        self.c.execute(update_jumlah_minuman, (str(new_jumlah_minuman), id_date, drink))
        self.conn.commit()

    def get_id_date_by_date(self, _date):
        get_id_tanggal = """
        SELECT Pesanan.ID_tanggal
        FROM Pesanan
        WHERE (((Pesanan.Tanggal)=?));
        """
        self.c.execute(get_id_tanggal, (_date,))
        rows = self.c.fetchall()
        return rows[0][0]

    def get_all_data_to_report_tab(self):
        statement_sql = """
        SELECT Pesanan.Tanggal, Detail_Pesanan.Menu_makanan, Detail_Pesanan.Jumlah_makanan, Detail_Pesanan.Menu_minuman, Detail_Pesanan.Jumlah_minuman
        FROM Pesanan INNER JOIN Detail_Pesanan ON Pesanan.ID_tanggal = Detail_Pesanan.ID_tanggal;
        """
        self.c.execute(statement_sql)
        rows = self.c.fetchall()

        order_dtos = []
        for (date, food, amt_food, drink, amt_drink) in rows:
            order_dtos.append(OrderDTO(food, drink, None, amt_food, amt_drink, None, date))

        return order_dtos
