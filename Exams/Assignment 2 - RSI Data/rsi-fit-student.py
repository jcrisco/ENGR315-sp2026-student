import pandas as pd
import numpy as np
from scipy.stats import norm, chisquare, ttest_ind, ttest_1samp
import matplotlib.pyplot as plt

"""
Preamble: Load data from source CSV file
"""
path_to_datafile = "../../data/drop-jump/all_participant_data_rsi.csv"

# To begin, we need to load the .csv file and make sure we know what data is in each column. After loading the data in the file,
# I'm going to print the headers to make suren that I know what data is in each column.
df = pd.read_csv(path_to_datafile) # this will read the .csv file and save it as a dataframe.
print(df.head()) # this line will print the headers in the .csv file... Based on this output we see that columns are called "trial",
# "force_plate_rsi", "accelerometer_rsi", "percent_error".

"""
Question 1: Load the force plate and acceleration based RSI data for all participants. Map each data set (accel and FP)
to a normal distribution. Clearly report the distribution parameters (mu and std) and generate a graph two each curve's 
probability distribution function. Include appropriate labels, titles, and legends.
"""
print('-----Question 1-----')

# Now we know that the "force plate and acceleration based RSI data" are saved under "force_plate_rsi", and "accelerometer_rsi",
# So, we are going to load that data from the dataframe(s) first...
accel_rsi_data = df['accelerometer_rsi'] # this line will create a variable of the accelerometer data.
force_plate_rsi_data = df['force_plate_rsi'] # this line will create a variable of the force plate data.
# Next, we are asked to map both of these data sets to a normal distribution, which we can do using the norm.fit() function...
mu_a, std_a = norm.fit(accel_rsi_data) # this line distinguishes mu and std for the accelerometer data by _a and then maps to normal distribution.
mu_fp, std_fp = norm.fit(force_plate_rsi_data) # this line distinguishes mu and std for the force plate data by _fp and then maps to normal distribution.
# Then, we need to make sure we know what mu_a, mu_fp, std_a, and std_fp are, so we're going to print them out...
print("For Accelerometer: mu =", mu_a, ", std =", std_a) # this line will print mu_a and std_a.
print("For Force Plate: mu =", mu_fp, ", std =", std_fp) # this line will print mu_fp and std_fp.
# Finally, we're going to generate a figure of this data...
# First, we need to give the x-axis values, we can find the min and max by printing the min() and max() of each variable...
# print("accel min:", accel_rsi_data.min(), "accel max:", accel_rsi_data.max()) # from this: min = 0, max = 1.35
# print("fp min:", force_plate_rsi_data.min(), "fp max:", force_plate_rsi_data.max()) # from this: min = 0, max = 1.241
# The two above lines will be ran to show me what my bounds need to be when we write np.linspace(start, stop, # of points)...
# (these lines are commented out so they dont clutter the output since they were only needed once)...
x = np.linspace(0, 1.5, 300) # I chose 0 and 1.5 as my bounds based on the above function outputs.
# Now we're ready to assemble the rest of the graph...
plt.figure(figsize=(10,5)) # set the size of the figure.
plt.plot(x, norm.pdf(x, mu_a, std_a), label='Accelerometer Distribution') # plot the variable x on the x-axis, and the normal distribution on the y-axis.
plt.plot(x, norm.pdf(x, mu_fp, std_fp), label='Force Plate Distribution') # plot the variable x on the x-axis, and the normal distribution on the y-axis.
plt.xlabel('RSI Data Value') # give x-axis a label.
plt.ylabel('Probability') # give y-axis a label.
plt.title('Normal Probability Distribution for Accelerometer Data and Force Plate RSI Data') # give the graph a title.
plt.legend() # plot the legend.
plt.savefig("Normal Distribution for A&FP RSI Data.png") # generate the plot.

"""
Question 2: Conduct a Chi2 Goodness of Fit Test for each dataset to test whether the data is a good fit
for the derived normal distribution. Clearly print out the p-value, chi2 stat, and an indication of whether it is 
a fit or not. Do this for both acceleration and force plate distributions. It is suggested to generate 9 bins between 
[0,2), add append -inf and +inf to both ends of the bins. An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 2-----')

# In order to conduct a Chisquared Goodness of Fit Test for the two datasets, we first need to establish our bins.
# These bins are essentially buckets that our data gets sorted into so that we can see how many points actually fell into the bucket,
# as opposed to how many points the normal distribution predicts should land in each bucket...
bins = np.linspace(0, 2, 10) # this line creates 9 evenly spaced bins from [0,2]
bins = np.concatenate([[-np.inf], bins, [np.inf]]) # this line adds in the boundaries of -inf and +inf to both sides of the bins, making sure all points are captured.
# We'll be using the same bins for both the Acceleration and Force Plate Data, which is why they are placed up here.
# We'll also be using the same alpha, so we're going to define it here as well...
alpha = 0.05
"""
Acceleration
"""

# Now that our bins are established, we need to count how many points from the data end up in our bins, which we can do using np.histogram()...
actual_a, _ = np.histogram(accel_rsi_data, bins=bins) # this line will count how many points are in each bin and save that as a variable,
# The histogram function will return the counts array as 'actual_a', and then it will try to return the bin edges which we don't want, so we use '_'.
# Next, we're going to use the norm.cdf() function, or the Cumulative Distribution Function to find the probability at every bin edge...
cdfvals_a = norm.cdf(bins, mu_a, std_a)
# Then, we need to find the expected counts for each bin. This can be done by taking the np.diff() between neighboring CDF values to find,
# the probability of each individual bin. If we take this result and multiply it by the length of the list (len()), those probabilities will be,
# converted into expected counts...
expected_a = np.diff(cdfvals_a) * len(accel_rsi_data) # this line finds the probability of each bin and then converts that into expected counts.
# Now we can finally run our Chisquared test to compare our actual_a and expected_a values...
chi2_stat_a, p_a = chisquare(actual_a, f_exp=expected_a) # this line finds our chi2 stat and p value, the larger the difference,
# the higher the chi2 stat, the lower the p-value (doesn't fit distribution well).
# Now we make sure that the p-value and chi2 stat are clearly shown...
print("Accelerometer chi2 stat =", chi2_stat_a, ", p =", p_a) # this line prints our p and chi2 values.
# Finally, we compare the p-value to the given alpha to determine if the data is a good fit or not...
if p_a > alpha:
    print("Accelerometer RSI data is a GOOD FIT")
else:
    print("Accelerometer RSI data is NOT A GOOD FIT")

"""
Force Plate
"""
# Now we are going to repeat the exact same process. The only changes that will be made are changing the arguments and variables,
# to make sure that they reflect/are referencing the force plate RSI data now...
actual_fp, _ = np.histogram(force_plate_rsi_data, bins=bins) # counts how many points are in each bin for the force plate data.
cdfvals_fp = norm.cdf(bins, mu_fp, std_fp) 
expected_fp = np.diff(cdfvals_fp) * len(force_plate_rsi_data) # finds expected counts for each bin.
chi2_stat_fp, p_fp = chisquare(actual_fp, f_exp=expected_fp) # finds chi2 stat and p value.
print("Force Plate chi2 stat =", chi2_stat_fp, ", p =", p_fp) # prints p and chi2.
# Lastly, determine if the data is a good fit or not, again...
if p_fp > alpha:
    print("Force Plate RSI data is a GOOD FIT")
else:
    print("Force Plate RSI data is NOT A GOOD FIT")

"""
Question 3: Perform a t-test to determine whether the RSI means for the acceleration and force plate data are equivalent 
or not. Clearly report the p-value for the t-test and make a clear determination as to whether they are equal or not.
An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 3-----')

# For the third and final question, we need to conduct a t-test using ttest_ind() to determine whether the RSI means for the,
# accelerometer and force plate data are significantly different from each other or not...
t_stat, p_val = ttest_ind(accel_rsi_data, force_plate_rsi_data) # this line will conduct the t-test and provide a t and p value.
print("Two-Sample T-Test: t =", t_stat, ", p =", p_val) # this line will clearly report the p-value and t-value for the t-test.
# Finally, we need to check if the p-value is greater than alpha. If p > alpha, then the means ARE NOT significantly different,
# if p < alpha, then the means ARE significantly different...
if p_val > alpha:
    print("Conclusion: the means ARE NOT significantly different at alpha = 0.05")
else:
    print("Conclusion: the means ARE significantly different at alpha = 0.05")

"""
Question 4: Calculate the RSI Error for the dataset where error is expressed as the difference between the 
Force Plate RSI measurement and the Accelerometer RSI measurement. Fit this error distribution to a normal curve and 
plot a histogram of the data on the same plot showing the fitted normal curve. Include appropriate labels, titles, and 
legends. The default binning approach from matplot lib with 16 bins is sufficient.
"""

### YOUR CODE HERE