from http.client import responses

import requests

API = "https://opensky-network.org/api/states/all"

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


def get_countries_and_aeroplanes_count():
    """получает список всех стран и количество самолетов в их воздушных пространствах"""
    response = requests.get(API)

    if response.status_code == 200:
        data = response.json()
        aircrafts = data.get('states', [])

        counter_dict = {}

        for aircraft in aircrafts:
            country = aircraft[2]
            if country not in counter_dict:
                counter_dict[country] = 1
            else:
                counter_dict[country] += 1
        return counter_dict
    else:
        print(f"Произошла ошибка {response.status_code}")
        return {}

def get_avg_speed():
    """получает среднюю скорость по самолетам"""
    response = requests.get(API)

    if response.status_code == 200:
        data = response.json()
        aircrafts = data.get('states', [])

        total_speed = 0.0
        valid_planes_count = 0

        for aircraft in aircrafts:
            speed = aircraft[9]

            if speed is not None:
                total_speed += speed
                valid_planes_count += 1
        avg_speed = total_speed / valid_planes_count
        return f"Средняя скорость самолетов {round(avg_speed, 2)} м/с"
    else:
        print(f"Произошла ошибка {response.status_code}")
        return []

def get_aeroplanes_with_higher_speed():
    """получает список всех самолетов, у которых скорост выше средней"""
    response = requests.get(API)

    if response.status_code == 200:
        data = response.json()
        aircrafts = data.get('states', [])

        total_speed = 0.0
        valid_planes_count = 0

        for aircraft in aircrafts:
            speed = aircraft[9]

            if speed is not None:
                total_speed += speed
                valid_planes_count += 1

        if valid_planes_count == 0:
            return []

        avg_speed = total_speed / valid_planes_count
        aeroplanes_with_higher_speed = []

        for aircraft in aircrafts:
            speed = aircraft[9]
            if speed is not None and speed > avg_speed:
                aeroplanes_with_higher_speed.append(aircraft)

        print(f"Найдено {len(aeroplanes_with_higher_speed)} самолетов со скоростью выше средней  {round(avg_speed, 2)}")
        return aeroplanes_with_higher_speed

    else:
        print(f"Произошла ошибка {response.status_code}")

