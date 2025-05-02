from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.transition import MDSwapTransition
from kivy.uix.screenmanager import FallOutTransition, NoTransition
from datetime import datetime
import os
import sqlite3
from kivy.utils import platform
from faker import Faker

from src.views.loginscreen import LoginScreen
from src.views.timerscreen import TimerScreen
from src.views.appbar import CustomAppBar
from src.views.mainscreen import MainScreen
from src.views.drawercontent import DrawerContent
from src.views.homescreen import HomeScreen
from src.views.spendingsscreen import SpendingsScreen, AddRowButton
from src.views.settingsscreen import SettingsScreen

Window.size = (380, 640)
fake = Faker()

class DatabaseConnection():
    
    def __init__(self, db):
        self.db = db
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db)
        self.pencil = self.conn.cursor()

    def create_or_open(self):
        try:
            self.connect()
        except:
            print("already connected")
        self.pencil.execute(
            '''CREATE TABLE IF NOT EXISTS spendings(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                store TEXT,
                product TEXT,
                amount INTEGER,
                price FLOAT
        )''')
        self.conn.commit()

    def reset(self):
        try:
            # Delete all rows from the table
            self.pencil.execute("DELETE FROM spendings")
            self.conn.commit()
            # print("Database reset successfully")
        except Exception as e:
            print(f"Failed to reset database: {e}")

    def custom_query_execution(self, query):
        self.pencil.execute(query)
        self.conn.commit()
        
    def custom_fetch_execution(self, query):
        self.pencil.execute(query)
        records = self.pencil.fetchall()
        return records
    
    def delete_row_by_id(self, id):
        query = f"""DELETE FROM spendings WHERE id = ?"""
        self.pencil.execute(query, (id,))
        self.conn.commit()
    
    def delete_rows_by_ids(self, ids):
        placeholders = ', '.join(['?'] * len(ids))
        query = f"""DELETE FROM spendings WHERE id IN ({placeholders})"""
        self.pencil.execute(query, ids)
        self.conn.commit()

    def update(self, id, new_values):
        query = f'''
        UPDATE spendings 
        SET date = ?, store = ?, product = ?, amount = ?, price = ?
        WHERE id = {id}
        '''
        try:
            self.pencil.execute(query, new_values)
            self.conn.commit()
        except Exception as e:
            print(f"Failed to update database: \n{e}")

        
    def get_id_from_row(self, row):
        query = """
        SELECT id 
        FROM spendings
        WHERE date = ? AND store = ? AND product = ? AND amount = ? AND price = ?
        """
        self.pencil.execute(query, row)
        result = self.pencil.fetchone()
        return result[0] if result else None

    def insert(self, row):
        self.pencil.execute('INSERT INTO spendings (date, store, product, amount, price) VALUES(?, ?, ?, ?, ?)', row)
        self.conn.commit()

    def select_all_data(self, exclude_id: bool = False):
        self.pencil.execute("""SELECT * FROM spendings""")
        records = self.pencil.fetchall()
        if exclude_id:
            records = [record[1:] for record in records]
            return records
        return records

    def select_data_from_date(self, date = datetime.now().date().strftime("%d/%m/%Y"), exclude_id: bool = False):
        self.pencil.execute("""SELECT * FROM spendings WHERE date = ?""", (date,))
        records = self.pencil.fetchall()
        # Exclude the first value of each tuple
        if exclude_id:
            records = [record[1:] for record in records]
            return records
        return records

    def close(self):
        if self.conn:
            self.conn.close()

class TimerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if platform == "android":
            self.__db_path = os.path.join(self.user_data_dir , "spendings.db") 
        else:
            self.__db_path = "src/db/spendings.db"
        print("plataform = ", platform)
        print(f"Database path set to: {self.__db_path}")
        self.my_database = DatabaseConnection(self.__db_path)
        self.root_app = Builder.load_file("main.kv")

    def on_start(self):
        try:
            self.my_database.create_or_open()
            self.my_database.connect()
            print("Database connection opened")
        except:
            print("Database connection failed")
        # finally:
        #     self.my_database.reset()

        # for _ in range(5):
        #     # fake_date = fake.date_this_month(before_today=True).strftime("%d/%m/%Y")
        #     fake_date = datetime.now().date().strftime("%d/%m/%Y")
        #     fake_store = fake.word()
        #     fake_product = fake.word()
        #     fake_amount = str(int(fake.unique.random_int(min = 1, max = 9)))
        #     fake_price = str(float(fake.unique.random_number()))
        #     fake_db_value = (fake_date, fake_store, fake_product, fake_amount, fake_price)
        #     print(fake_db_value)
        #     self.my_database.insert(fake_db_value)

    def on_stop(self):
        try:
            self.my_database.close()
            print("Database connection closed")
        except:
            print("Database connection failed")
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"

        return self.root_app

if __name__ == "__main__":
    TimerApp().run()
