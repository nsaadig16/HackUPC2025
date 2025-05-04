import sqlite3
class SQLiteConnector:
    conn= None
    def __init__(db_name="my_database.db"):
        """Connect to the SQLite database (or create it if it doesn't exist)."""
        if SQLiteConnector.conn is None:
            SQLiteConnector.conn = sqlite3.connect('db.db')
            SQLiteConnector.create_table()
        #return SQLiteConnector.conn
    def create_table():
        """Create a sample table."""
        cursor = SQLiteConnector.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS slides (
                id INTEGER PRIMARY KEY,
                ord INTEGER,
                votes_up INTEGER DEFAULT 0,
                votes_down INTEGER DEFAULT 0,
                content TEXT
            );""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itinerary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT
            );""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS travel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT
            );""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flight (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT
            );
        """)
        SQLiteConnector.conn.commit()
    def insert(type: str, content: str, ord: int = None):
        """Insert a new user into the users table."""
        cursor = SQLiteConnector.conn.cursor()
        if ord is None:
            #cursor.execute('INSERT INTO ' + type +' (content, ord) VALUES (\''+str(content)+'\')')
            print(f'INSERT INTO {type} (content, ord) VALUES ("{str(content)}")')
            cursor.execute(f'INSERT INTO {type} (content) VALUES ("{str(content)}")')
        else:
            print(str(ord))
            cursor.execute("INSERT INTO " + type +" (content, ord) VALUES (\""+str(content)+"\", "+ord+")")
        SQLiteConnector.conn.commit()
        return cursor.lastrowid
    def get_all(type: str):
        """Retrieve all users from the users table."""
        cursor = SQLiteConnector.conn.cursor()
        if type == "slides":
            cursor.execute(f"SELECT * FROM {type} ORDER BY ord")
        else:
            cursor.execute(f"SELECT * FROM {type}")
        return cursor.fetchall()
    def get(type: str, id: int):
        """Retrieve all users from the users table."""
        cursor = SQLiteConnector.conn.cursor()
        cursor.execute(f"SELECT * FROM {type} WHERE id = {id}")
        return cursor.fetchall()
    def get_by_order(type: str, ord: int):
        """Retrieve all users from the users table."""
        cursor = SQLiteConnector.conn.cursor()
        cursor.execute(f"SELECT * FROM {type} WHERE ord = {ord}")
        return cursor.fetchall()
    def replace(type: str, id: int, content: str):
        """Retrieve all users from the users table."""
        cursor = SQLiteConnector.conn.cursor()
        cursor.execute(f"UPDATE {type} SET content = {content} WHERE id = {id}")
        return cursor.fetchall()
    def delete(type: str, id: int):
        """Retrieve all users from the users table."""
        cursor = SQLiteConnector.conn.cursor()
        cursor.execute(f"DELETE FROM {type} WHERE id = {id}")
        return cursor.fetchall()
    def vote_up(ord: int):
        """Retrieve all users from the users table."""
        cursor = SQLiteConnector.conn.cursor()
        cursor.execute(f"UPDATE slides SET votes = votes + 1 WHERE ord = {ord}")
        return cursor.fetchall()
    def vote_down(ord: int):
        """Retrieve all users from the users table."""
        cursor = SQLiteConnector.conn.cursor()
        cursor.execute(f"UPDATE slides SET votes = votes - 1 WHERE order = {ord}")
        return cursor.fetchall()
SQLiteConnector()