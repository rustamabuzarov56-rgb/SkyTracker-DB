import requests
import psycopg2

API = "https://opensky-network.org/api/states/all"
TARGET_COUNTRIES = ['France', 'Germany', 'Italy', 'Spain']

def get_all_aeroplanes():
    """получает список всех воздушных судов"""
    response = requests.get(API)

    if response.status_code == 200:
        data = response.json()
        aircrafts = data.get('states', [])
        print(f"В воздухе сейчас находится {len(aircrafts)} самолетов")
        return aircrafts
    else:
        print(f"Произошла ошибка {response.status_code}")
        return []


def get_country_coordinates(country_name):
    """получает название страны и возвращает ее координаты"""
    API_nominatim = f"https://nominatim.openstreetmap.org/search?q={country_name}&format=json&limit=1"
    headers = {
        "User-Agent": 'SkyTracker-DB/1.0'
    }

    response = requests.get(API_nominatim, headers=headers)

    if response.status_code == 200:
        data = response.json()

        if data:
            lat = data[0].get('lat')
            lon = data[0].get('lon')
            return float(lat), float(lon)
        if not data:
            return None
    else:
        print(f"Произошла ошибка {response.status_code}")
        return None

def filter_aircrafts_by_countries(aircrafts_list):
    """оставляет тлолько те самолеты, которые летят над выбранными странами"""
    filtered_aircrafts = []

    for aircraft in aircrafts_list:
        country = aircraft[2]
        if country in TARGET_COUNTRIES:
            filtered_aircrafts.append(aircraft)

    return filtered_aircrafts

def create_tables(conn):
    """создает таблицы для стран и самолетов в базе данных SQL, если их еще нету"""
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS countries (
                    country_name VARCHAR(100) PRIMARY KEY,
                    latitude FLOAT,
                    longitude FLOAT);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS aircrafts (
                    id SERIAL PRIMARY KEY,
                    icao24 VARCHAR(10),
                    callsign VARCHAR(20),
                    country VARCHAR(100),
                    speed FLOAT);""")

    conn.commit()
    cur.close()

def save_data_to_db(country_coordinate, filtered_aircrafts, conn):
    """записывает отфильтрованные самолеты и координаты стран в БД"""
    cur = conn.cursor()
    for country_name, coords in country_coordinate.items():
        cur.execute("""INSERT INTO countries (country_name, latitude, longitude)
         VALUES (%s, %s, %s);""", (country_name, coords['lat'], coords['lon']))

    for aircraft in filtered_aircrafts:
        icao24 = aircraft[0]
        callsign = aircraft[1].strip() if aircraft[1] else None
        country = aircraft[2]
        speed = aircraft[9]

        cur.execute("""INSERT INTO aircrafts (icao24, callsign, country, speed)
        VALUES (%s, %s, %s, %s)""", (icao24, callsign, country, speed))
    conn.commit()
    cur.close()