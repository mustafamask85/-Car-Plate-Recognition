import mysql.connector 
from mysql.connector import Error 
from datetime import datetime


def manage_number_platte(numberplate):

    host = 'localhost'
    user = 'root'
    password = 'root'
    database = 'numberplate'

    connection = None

    try: 
        print("Attempting to connect to MySQL Server...")
       
        connection = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
        )
        if connection.is_connected():
            print("Connection to MySQL Server successful")
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            connection.database = database

            create_table_query = """

            CREATE TABLE IF NOT EXISTS numberplate (
            
                id INT AUTO_INCREMENT PRIMARY KEY,
                numberplate TEXT NOT NULL,
                entry_date DATE,
                entry_time TIME
            )

        """
            cursor.execute(create_table_query)
            connection.commit()



            insert_data_query = """

                INSERT INTO numberplate (numberplate,entry_date,entry_time)
                VALUES(%s,%s,%s)

                """
            current_date = datetime.now().date()
            current_time = datetime.now().time()
            data = (numberplate,current_date,current_time)

            cursor.execute(insert_data_query,data)
            connection.commit()

            fetch_data_query = "SELECT * FROM numberplate"
            cursor.execute(fetch_data_query)
            result = cursor.fetchall()
    except Error as e:
        print(f"Error: '{e}'")

    cursor.close()
    connection.close()
