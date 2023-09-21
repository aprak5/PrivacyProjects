"""
File DiffPrivacy.py
Author: Amit Prakash (aprakas5) and Anupam Das (adas8)
Purpose: This file works with some data from a Illinois (IL) employee salary data.
This file works to inject noise in the data to ensure no sensitive data is directly exposed. 
This is accomplished by using differential privacy and a Laplace distribution to inject noise in the data (distribution).
"""

# Import all necessary modules/libraries
import pandas as pd
from diffprivlib import tools as dp
import matplotlib.pyplot as plt

# Read the data from the file to a dataframe
data = pd.read_csv(r'IL_employee_salary.csv')   
hist, bins = dp.histogram(data.get("Annual Salary")) # epsilon = 1
# Plot the data with the original histogram
plt.bar(bins[:-1], hist, width=(bins[1]-bins[0]) * 0.9)
plt.show()

# Plot the data with different epsilon values (0.05, 0.1, 5)
for ep in [0.05, 0.1, 5]:
    dp_hist, dp_bins = dp.histogram(data.get("Annual Salary"), epsilon=ep)
    plt.bar(dp_bins[:-1], dp_hist, width=(dp_bins[1]-dp_bins[0]) * 0.9)
    plt.show()

