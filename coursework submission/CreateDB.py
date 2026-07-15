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

    # Task 3 requires that we use SQL Change Tracking, which in turn requires that 
    # there be a primary key present in the WeatherData table. Originally, the
    # primary key was set to be sensor_id, but this caused problems because in the
    # AutomatedSimulateData route, multiple readings are inserted for the same sensor_id,
    # which was causing a primary key violation. Table is modified to have a new 
    # primary key reading_id which is an IDENTITY column that auto-increments with each
    # new reading inserted into the database. reading_id isn't ever used in the Azure
    # Function app, but is necessary to enable SQL Change Tracking.

    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='WeatherData' AND xtype='U')
    CREATE TABLE WeatherData (
        reading_id INT PRIMARY KEY IDENTITY(1,1),
        sensor_id INT,
        temperature FLOAT,
        wind_speed FLOAT,
        humidity FLOAT,
        co2_level INT,
        timestamp DATETIME DEFAULT GETDATE()
    );               
    """)

    conn.commit()

    print("Table 'WeatherData' created successfully or already exists.")

except Exception as e:
    print("Error occured:", e)

finally:
    try:
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error occurred while closing connections:", e)
