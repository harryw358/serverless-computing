import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


# --- Graph 1 (Task 1): Average Elapsed Time against Number of Concurrent Users

# Define the user counts to process data for
user_counts = [1, 10, 50, 100, 500, 1000]

# Initialise lists to store average elapsed times
avg_elapsed_times = []

# Reads each CSV file and calculate average elapsed time
for count in user_counts:
    filepath = os.path.join('./apache-jmeter-5.6.3/bin/test1_results', f'{count}_users.csv')

    df = pd.read_csv(filepath)
    avg_elapsed_times.append(df['elapsed'].mean())

# Create the plot
plt.figure(figsize = (10, 6))
plt.title('Average Elapsed Time vs  Number of Users (Test 1)')
plt.xlabel('Number of Concurrent Users (1 user = 20 simulated sensors)')
plt.ylabel('Average Elapsed Time (ms)')

# Plot line with data
plt.plot(user_counts, avg_elapsed_times, marker = 'o')
plt.xticks(user_counts)
plt.xscale('log') # Log scale is better for visualising the graph
plt.grid(True)
plt.savefig('test1_average_elapsed_time.png', dpi = 400)
plt.show()

# --- Graph 2 (Task 2): Average Elapsed Time against Number of Readings in Database

# Define the data sizes to process data for
data_sizes = [100, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

# Initialise list to store elapsed times
elapsed_times = []

# Reads each CSV file and extracts elapsed time
for size in data_sizes:
    filepath = os.path.join('./apache-jmeter-5.6.3/bin/test2_results', f'{size}_readings.csv')

    df = pd.read_csv(filepath)
    elapsed_times.append(df['elapsed'])

# Create the plot
plt.figure(figsize = (10, 6))
plt.title('Elapsed Time vs Number of Readings in Database (Test 2)')
plt.xlabel('Number of Readings in SQL Database')
plt.ylabel('Elapsed Time (ms)')

# Plot line with data
plt.plot(data_sizes, elapsed_times, marker = 'o')
plt.xticks(data_sizes)
plt.grid(True)
plt.ylim(bottom = 0) # makes y-axis start at 0 for better visualisation
# plt.xscale('log')
plt.savefig('test2_elapsed_time.png', dpi = 400)
plt.show()

