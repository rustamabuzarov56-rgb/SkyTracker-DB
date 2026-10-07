import psycopg2
import time
from src.parser import (TARGET_COUNTRIES, get_all_aeroplanes, get_country_coordinates, filter_aircrafts_by_countries, \
    create_tables, save_data_to_db)
from src.db_manager import DBManager

def main():
    print("Процесс запуска сбора данных...")

    conn = psycopg2.connect(
        dbname="skytracker",
        user="postgres",
        password="0852",
        host="localhost",
        port="5432"
    )
    create_tables(conn)
    print("Таблицы в базе данных созданы")

    geo_data = {}
    print("Сбор геоданных стран из Nominatim API...")

    for country in TARGET_COUNTRIES:
        geo_data[country] = get_country_coordinates(country)
        time.sleep(1)

    print("Скачивание данных о самолетах из OpenSky API...")
    all_aircrafts = get_all_aeroplanes()
    print("Фильтрация самолетов...")
    filtered_aircrafts = filter_aircrafts_by_countries(all_aircrafts)
    save_data_to_db(geo_data, filtered_aircrafts, conn)

    print("Запуск аналитики из класса DBManager")

    db = DBManager(
        dbname="skytracker",
        user="postgres",
        password="0852",
        host="localhost",
        port="5432"
    )

    avg_speed = db.get_avg_speed()
    print(f"Средняя скорость всех самолетов в базе: {avg_speed} м/с")

    print("Статистика по странам (Координаты и количество самолетов)")
    country_stats = db.get_countries_and_aeroplanes_count()
    for row in country_stats:
        name = row[0]
        lat = row[1]
        lon = row[2]
        count = row[3]
        print(f"Страна {name} (широта {lat}, долгота {lon}) | самолетов в небе {count}")

        keyword = "ACA"
        found_aircrafts = db.get_aeroplane_with_keyword(keyword)
        print(f"Поиск по позывному {keyword}: найдено {len(found_aircrafts)} самолетов")


    conn.close()
    print("База данных успешно заполнена свежими данными! Все соединения закрыты.")

if __name__ == "__main__":
    main()