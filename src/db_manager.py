import psycopg2




class DBManager:
    """Менеджер для выполнения SQL-запросов и анализа данных в БД PostgreSQL"""

    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def get_countries_and_aeroplanes_count(self):
        """получает список всех стран и количество самолетов в их воздушных пространствах"""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT c.country_name, c.latitude, c.longitude, COUNT(a.id) AS plane_count
                           FROM countries c
                           LEFT JOIN aircrafts a ON c.country_name = a.country
                           GROUP BY c.country_name, c.latitude, c.longitude""")
            result = cur.fetchall()
            return result

    def get_all_aeroplanes(self):
        """получает список всех воздушных судов"""
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM aircrafts")
            result = cur.fetchall()
            return result

    def get_avg_speed(self):
        """получает среднюю скорость по самолетам"""
        with self.conn.cursor() as cur:
            cur.execute("SELECT AVG(speed) FROM aircrafts")
            result = cur.fetchone()
            if result and result[0] is not None:
                return round(result[0], 2)
            return 0.0

    def get_aeroplanes_with_higher_speed(self):
        """получает список всех самолетов, у которых скорость выше средней"""
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM aircrafts WHERE speed > (SELECT AVG(speed) FROM aircrafts)")
            result = cur.fetchall()
            return result

    def get_aeroplane_with_keyword(self, keyword):
        """получает список всех самолетов, в позывном которых содержатся переданные в метод символы"""
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM aircrafts WHERE callsign ILIKE %s", (f"%{keyword}%",))
            result = cur.fetchall()
            return result
