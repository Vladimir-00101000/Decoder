import mysql.connector
from config import host_id, user_name, password, db_name

values_to_db = [
    (55.75321, 37.619055),
    (38.870985, -77.056034),
    (-22.89169, -43.217589),
    (-35.308288, 149.124273),
    (45.234673, -98.345231)
]

db_connection = mysql.connector.connect(
    host = host_id,
    user = user_name,
    password = password,
    database = db_name
)

# clearing the table
with db_connection.cursor() as cursor:
    cursor.execute("""DELETE FROM address""")
    db_connection.commit()

# Filling in the table
with db_connection.cursor() as cursor:
    for x, y in values_to_db:
        fill_table = f"INSERT INTO address (point) VALUES (POINT({x}, {y}))"
        cursor.execute(fill_table)
    db_connection.commit()
