import sqlite3


class DB:
    def __init__(self):
        self.orders = sqlite3.connect(r'list/orders.db', check_same_thread=False)
        self.orders_cursor = self.orders.cursor()

    def add_to_db(self, user_id, deliver_id, food_id, count, food_size, price, address, status):
        self.orders_cursor.execute("INSERT INTO orders VALUES(?, ?, ?, ?, ?, ?, ?, ?);",
                                   (user_id, deliver_id, food_id, count, food_size, price, address, status))
        self.orders.commit()
