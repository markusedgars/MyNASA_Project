import mysql.connector
from configparser import ConfigParser

def column_exists(cursor, table, column):
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.columns
        WHERE table_name = %s AND column_name = %s
    """, (table, column))
    return cursor.fetchone()[0] > 0

# Load database configuration from config.ini
config = ConfigParser()
config.read('config.ini')

db_config = {
    'host': config.get('mysql_config', 'mysql_host'),
    'database': config.get('mysql_config', 'mysql_db'),
    'user': config.get('mysql_config', 'mysql_user'),
    'password': config.get('mysql_config', 'mysql_pass')
}

# Connect to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Check if the column already exists
if not column_exists(cursor, 'ast_daily', 'is_visible'):
    # SQL command for the migration
    migration_sql = """
    ALTER TABLE ast_daily
    ADD COLUMN is_visible TINYINT(1) NOT NULL DEFAULT 0;
    """

    # Executing the migration
    try:
        cursor.execute(migration_sql)
        connection.commit()
        print("Migration executed successfully.")
    except mysql.connector.Error as err:
        print(f"Error occurred during migration: {err}")
else:
    print("Column 'is_visible' already exists in 'ast_daily'. No migration needed.")

cursor.close()
connection.close()
