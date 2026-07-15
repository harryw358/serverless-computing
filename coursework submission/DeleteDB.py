# Python script to delete the SQL database WeatherData table

import pyodbc

conn_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:myfreesqlserver638.database.windows.net,1433;"
    "Database=weather-info;"
    "Uid=myfreesqlserver638;"
    "Pwd=Duzvyh-0myzti-wynpuq;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

try:
    conn = pyodbc.connect(conn_string)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS WeatherData;")

    conn.commit()
    print("Table 'WeatherData' deleted successfully if exists.")

except Exception as e:
    print("Error occured:", e)

finally:
    try:
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error occurred while closing connections:", e)

