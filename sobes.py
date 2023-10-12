import mysql.connector
from config import host_id, user_name, password, db_name
import requests

api_key ='iPE3drx58ceAhnIamPSS0SGhfffpjvHq'

db_connection = mysql.connector.connect(
    host = host_id,
    user = user_name,
    password = password,
    database = db_name
)

# We read the coordinates and get the result of the request URL
with db_connection.cursor() as cursor:
    cursor.execute("""SELECT ST_X(Point), ST_Y(Point)
                        FROM address
                       WHERE country IS NULL;
                    """)
    for latitude, longitude in cursor.fetchall():
        url = f'https://www.mapquestapi.com/geocoding/v1/reverse?key={api_key}&location={latitude}%2C{longitude}&outFormat=json&thumbMaps=false'
        response = requests.get(url)

        # Checking the success of the request
        if response.status_code == 200:
            data = response.json()
            # Extracting the address from the API response
            try:
                country = data['results'][0]['locations'][0]['adminArea1']
                city = data['results'][0]['locations'][0]['adminArea5']
            except IndexError:
                print('Incorrect coordinate format...')

            # We record the results in the database
            with db_connection.cursor() as cursor:
                data_recording = f"UPDATE address SET country = '{country}', city = '{city}'\
                                    WHERE ST_X(Point) = {latitude}"
                cursor.execute(data_recording)
                db_connection.commit()
        else:
            print(f'Ошибка при выполнении запроса: {response.status_code}')
