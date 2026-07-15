#!/bin/zsh

# Test script 1 copied here for submission

# For run_test1.sh, run_test2.sh, and run_test3.sh the setting up of the test plan is inspired by
# the official Apache JMeter documentation, available at: https://jmeter.apache.org

# --- Test 1 (Task 1): Demonstrating results in terms of scalability. In this case
# its showing how increasing the number of sensor readings impacts the performance
# of the SimulateData function. Could manually change sensor_id in the code and use 
# a timer object but using this seems more fun and professional. This test script runs the 
# JMeter test plan with the number of users specified in the current iteration of the 
# loop. 1 user = 20 simulated sensor readings. Users run concurrently so if there were 
# 50 users calling the endpoint simultaneously, thats 50 x 20 = 1000 calls.

# This test script needs to run in the same directory as the Apache JMeter bin directory

# In this script and the JMeter GUI, setting up the test plan to allow the user count to be entered in the command line is 
# inspired by the offical Apache JMeter documentation in section 3.12 Using Variables to parametrise tests of Elements of a Test Plan,
# available at: https://jmeter.apache.org/usermanual/test_plan.html

# 1 JMeter user = 20 simulated sensors
USER_COUNTS=(1 10 50 100 500 1000)

# Loop through each user count
for USERS in "${USER_COUNTS[@]}"; do
	echo "--- Running test with $USERS x 20 simulated sensors ---"

	# Run the test and output results to a temp results file
	./../jmeter -n \
		-t ./../test1.jmx \
		-l ./../temp_results.csv \
		-Jusers=$USERS

	# For Test 1, there will be 6 files of results to easily distinguish user count when generating graph
	if [[ $USERS -eq 1 ]]; then
		# Move temp file contents to actual results file which will be easier to find when generating graphs
		cat ./../temp_results.csv > ./../test1_results/1_users.csv
	elif [[ $USERS -eq 10 ]]; then
		# Repeat for other user counts
		cat ./../temp_results.csv > ./../test1_results/10_users.csv
	elif [[ $USERS -eq 50 ]]; then
		cat ./../temp_results.csv > ./../test1_results/50_users.csv
	elif [[ $USERS -eq 100 ]]; then
		cat ./../temp_results.csv > ./../test1_results/100_users.csv
	elif [[ $USERS -eq 500 ]]; then
		cat ./../temp_results.csv > ./../test1_results/500_users.csv
	elif [[ $USERS -eq 1000 ]]; then
		cat ./../temp_results.csv > ./../test1_results/1000_users.csv
	fi

	# Delete temp file
	rm ./../temp_results.csv
done

echo "--- All tests are complete. Data is stored in test1_results directory  ---"