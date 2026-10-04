import psycopg2




class DBManager:

    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def get_all_aeroplanes(self):
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

    def get_countries_and_aeroplanes_count(self):
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

    def get_avg_speed(self):
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

    def get_aeroplanes_with_higher_speed(self):
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

            print(
                f"Найдено {len(aeroplanes_with_higher_speed)} самолетов со скоростью выше средней  {round(avg_speed, 2)}")
            return aeroplanes_with_higher_speed

        else:
            print(f"Произошла ошибка {response.status_code}")
            return []

    def get_aeroplane_with_keyword(self, keyword):
        """получает список всех самолетов, в позывном которых содержатся переданные в метод символы"""
        response = requests.get(API)

        if response.status_code == 200:
            data = response.json()
            aircrafts = data.get('states', [])

            aeroplane_with_keyword = []

            for aircraft in aircrafts:
                callsign = aircraft[1]

                if callsign is not None:
                    if keyword.lower() in callsign.lower():
                        aeroplane_with_keyword.append(aircraft)
            return aeroplane_with_keyword
        else:
            print(f"Произошла ошибка {response.status_code}")
            return []
