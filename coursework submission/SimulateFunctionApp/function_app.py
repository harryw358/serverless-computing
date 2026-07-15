import azure.functions as func
import logging
import random
import pyodbc
import requests
import json
import os
import numpy as np
import datetime

app = func.FunctionApp()

# To run the application: Start in the coursework directory. If you want to
# reset the database to it's initial state, run DeleteDB.py, then CreateDB.py,
# then EnableSQLTracking.py. To start the function app, change to the SimulateFunctionApp
# directory and run "func start" in the terminal. You can also do this using the Azure tab
# in VS Code. The function app will start running locally and you can test the HTTP endpoints 
# manually by clicking on the links or entering them into your web browser. 

# Application flow: Every 10 seconds, the AutomatedSimulateData timer trigger
# calls the SimulateData HTTP trigger to generate 20 new sensor readings and
# insert them into the WeatherData table in the Azure SQL Database. The GetChanges
# SQL Trigger function is called automatically whenever new data is inserted into
# the WeatherData table, and recalculates the minimum, maximum, and average values for
# each field for each sensor, including newly uploaded data.


# SQL Trigger function will detect changes in the WeatherData table and recalculate
# minimum, maximum, and average for each field including the new data in the table. 
# This function is adapted from code provided in the official Microsoft documentation available
# at: https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-azure-sql-trigger?tabs=isolated-process%2Cpython-v2%2Cportal&pivots=programming-language-python
@app.sql_trigger(arg_name = "changes", connection_string_setting="SqlConnectionStringSQLTrigger", table_name="WeatherData")
def GetChanges(changes: str) -> None:
    # logging.info("SQL Changes: %s", json.loads(changes))
    logging.info("Changes detected in the WeatherData table. Recalculating min, max, avg for each field for each sensor.")

    # Call the QueryData HTTP endpoint
    url = "http://localhost:7071/api/QueryData"
    try:
        r = requests.get(url)
        logging.info(f"HTTP request to QueryData returned status code {r.status_code}")

    except Exception as e:
        logging.error(f"Error occurred while calling QueryData endpoint: {e}")

# Timer trigger function will call the SimulateData HTTP endpoint every 10 seconds
# to generate and insert new random sensor data into the WeatherData table.
@app.timer_trigger(schedule=f"*/10 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def AutomatedSimulateData(myTimer: func.TimerRequest) -> None:
    logging.info("AutomatedSimulateData timer trigger function ran.")

    # Call the SimulateData HTTP endpoint
    url = "http://localhost:7071/api/SimulateData"
    try:
        r = requests.get(url)
        logging.info(f"HTTP request to SimulateData returned status code {r.status_code}")
    except Exception as e:
        logging.error(f"Error occurred while calling SimulateData endpoint: {e}")

# HTTP trigger function will generate 20 random sensor readings and insert them
# into the WeatherData table in the Azure SQL Database.
@app.route(route="SimulateData", auth_level=func.AuthLevel.FUNCTION)
def SimulateData(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Adding a query parameter "sensors" which may be a part of the URL lets us determine how many readings per sensors to generate
    readings = req.params.get('readings')
    # Default to 20 if no paramter is provided
    try:
        readings = int(readings) if readings else 20
    except:
        return func.HttpResponse("Invalid readings parameter. Please provide an integer value.", status_code=400)

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
        cursor.fast_executemany = True

        data = []

        for i in range(readings):
            # Loop through sensor IDs 1 to 20
            sensor_id = (i % 20) + 1 # Sensor IDs range from 1 to 20
            temperature = round(random.uniform(5, 18), 2)
            wind_speed = round(random.uniform(12, 24), 2)
            humidity = round(random.uniform(30, 60), 2)
            co2_level = round(random.uniform(400, 1600), 2)

            cursor.execute("""
                INSERT INTO WeatherData (sensor_id, temperature, wind_speed, humidity, co2_level)
                VALUES (?, ?, ?, ?, ?)
            """, sensor_id, temperature, wind_speed, humidity, co2_level)

        conn.commit() 
        message = f"Inserted {readings} simulated sensor readings successfully."

        return func.HttpResponse(message, status_code=200)
    
    except Exception as e:
        logging.error(f"Error occured inserting data: {e}")
        return func.HttpResponse(f"Error occured inserting data: {e}", status_code=500)
    
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception as e:
            logging.error(f"Error occurred while closing connections: {e}")

# HTTP trigger just queries all data in the WeatherData table and 
# calculates the minimum, maximum, and average for each field for 
# each sensor, and outputs the results to the terminal.
@app.route(route="QueryData", auth_level=func.AuthLevel.FUNCTION)
def QueryData(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

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

        # Loop over all 20 sensors
        # Fetch all readings with the sensor_id i
        # Use cursor to retreive the data
        # Calculate the minimum, maximum, and average for each field for that current sensor
        # Output results to console

        for i in range(1, 21):
            cursor.execute("""
            SELECT sensor_id, temperature, wind_speed, humidity, co2_level FROM WeatherData  
            WHERE sensor_id = ?
            """, i)

            rows = cursor.fetchall()

            # Each row will have a length equal to the number of records that sensor
            # In each row, iterate through the records and extract the temp, wind_speed, humidity, co2_level
            # Store the values in separate lists
            temperatures = []
            wind_speeds = []
            humidities = []
            co2_levels = []

            length = len(rows)
            for x in range(length):
                temperatures.append(rows[x][1])
                wind_speeds.append(rows[x][2])
                humidities.append(rows[x][3])
                co2_levels.append(rows[x][4])

            print(f"Sensor ID: {i}")

            # Calculate min, max, avg for each sensor id
            min_temp = min(temperatures)
            max_temp = max(temperatures)
            avg_temp = sum(temperatures) / length

            min_wind = min(wind_speeds)
            max_wind = max(wind_speeds)
            avg_wind = sum(wind_speeds) / length

            min_humidity = min(humidities)
            max_humidity = max(humidities)
            avg_humidity = sum(humidities) / length

            min_co2 = min(co2_levels)
            max_co2 = max(co2_levels)
            avg_co2 = sum(co2_levels) / length

            # Print results to terminal
            print(f"Temperature - Min: {min_temp}, Max: {max_temp}, Avg: {avg_temp:.2f}")
            print(f"Wind Speed - Min: {min_wind}, Max: {max_wind}, Avg: {avg_wind:.2f}")
            print(f"Humidity - Min: {min_humidity}, Max: {max_humidity}, Avg: {avg_humidity:.2f}")
            print(f"CO2 Level - Min: {min_co2}, Max: {max_co2}, Avg: {avg_co2:.2f}")
            print("=====================================")


        message = "WeatherData query completed successfully. Results printed to terminal."
        return func.HttpResponse(message, status_code=200)
    
    except Exception as e:
        logging.error(f"")
        return func.HttpResponse(f"Error occured retrieiving data", status_code=500)
    
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception as e:
            logging.error(f"Error occurred while closing connections: {e}")

