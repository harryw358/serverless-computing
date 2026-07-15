#!/bin/zsh

# Test script 2 copied here for submission

# For run_test1.sh, run_test2.sh, and run_test3.sh the setting up of the test plan is inspired by
# the official Apache JMeter documentation, available at: https://jmeter.apache.org

# --- Test 2 (Task 2): Demonstrating performance in terms of scalability when the amount of data
# being processed for analysis increases. In this case its showing how increasing the amount
# of data being queried by the QueryData function impacts performance. The SQL databases will
# be populated with various amounts of data before running the tests. The test script will run
# a for loop over 100 readings, 1000 readings, and 10,000 readings. Each iteration of the loop, all data in the database will be deleted, and 
# repopulated with the required amount of data. Then the JMeter test plan will record the elapsed
# time being 1 user making a request to the QueryData endpoint and a request being received.

# This test script needs to run in the same directory as the Apache JMeter bin directory

# In this script and the JMeter GUI, setting up the test plan to allow the user count to be entered in the command line is 
# inspired by the offical Apache JMeter documentation in section 3.12 Using Variables to parametrise tests of Elements of a Test Plan,
# available at: https://jmeter.apache.org/usermanual/test_plan.html

DATA_SIZES=(100 1000 2000 3000 4000 5000 6000 7000 8000 9000 10000)

# Reset database to initial state before starting tests
python ../../../DeleteDB.py

for DATA in "${DATA_SIZES[@]}"; do
    echo "--- Running test with $((DATA)) sensor readings in SQL database ---"

    # (1) Create database
    python ../../../CreateDB.py
    # (2)  Enable change tracking 
    python ../../../EnableSQLTracking.py
    # (3) Call SimualateData endpoint with readings parameters = DATA
    curl "http://localhost:7071/api/SimulateData?readings=$((DATA))"

    # (4) Run the test and output results to a temp results file
    # Come out of test scripts directory to run JMeter
    ./../jmeter -n \
        -t ./../test2.jmx \
        -l ./../temp_results.csv \
        -Jusers=1

    # (5) Store results
    # For Test 2, there will be 5 files of results to easily distinguish size of database when generating graph
    if [[ $DATA -eq 100 ]]; then
        # Move temp file contents to actual results file  which will be easier to find when generating graph
        cat ./../temp_results.csv > ./../test2_results/100_readings.csv
    elif [[ $DATA -eq 1000 ]]; then
        # Repeat for other data sizes
        cat ./../temp_results.csv > ./../test2_results/1000_readings.csv
    elif [[ $DATA -eq 2000 ]]; then
        cat ./../temp_results.csv > ./../test2_results/2000_readings.csv
    elif [[ $DATA -eq 3000 ]]; then
        cat ./../temp_results.csv > ./../test2_results/3000_readings.csv
    elif [[ $DATA -eq 4000 ]]; then
        cat ./../temp_results.csv > ./../test2_results/4000_readings.csv
    elif [[ $DATA -eq 5000 ]]; then
        cat ./../temp_results.csv > ./../test2_results/5000_readings.csv
    elif [[ $DATA -eq 6000 ]]; then
        cat ./../temp_results.csv > ./../test2_results/6000_readings.csv
    elif [[ $DATA -eq 7000 ]]; then
        cat ./../temp_results.csv > ./../test2_results/7000_readings.csv
    elif [[ $DATA -eq 8000 ]]; then
        cat ./../temp_results.csv > ./../test2_results/8000_readings.csv
    elif [[ $DATA -eq 9000 ]]; then
        cat ./../temp_results.csv > ./../test2_results/9000_readings.csv
    elif [[ $DATA -eq 10000 ]]; then
        cat ./../temp_results.csv > ./../test2_results/10000_readings.csv
    fi

    # Delete temp file
    rm ./../temp_results.csv

    # Delete database before next test
    python ../../../DeleteDB.py
done

echo "--- All tests are complete. Data is stored in test2_results directory  ---"