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

    # The code used to enable change tracking is adapted from code provided in
    # the official Microsoft documentation available 
    # at: https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-azure-sql-trigger?tabs=isolated-process%2Cpython-v2%2Cportal&pivots=programming-language-python
    cursor.execute("""
    ALTER TABLE WeatherData
    ENABLE CHANGE_TRACKING
    """)

    cursor.commit()

    print("SQL tracking for table 'WeatherData' was enabled successfully.")

except Exception as e:
    print("Error occured:", e)

finally:
    try:
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error occurred while closing connections:", e)
