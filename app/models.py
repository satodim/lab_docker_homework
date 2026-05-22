import os
import mysql.connector

class ItemModel:
    def __init__(self):
       
        self.config = {
            'host': os.environ.get('DB_HOST'),
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'database': os.environ.get('DB_NAME')
        }
        
        if not all(self.config.values()):
            raise ValueError("Missing required environment variables: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME")

    def get_all_items(self):
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT name FROM items')
            items = cursor.fetchall()
            cursor.close()
            conn.close()
            return items
        except Exception as e:
            print(f"Database error: {e}")
            return []
