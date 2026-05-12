import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import norm, chisquare
import math

print(f"----- Question 1 -----")
# Create a variable of the filepath to subject-info.csv
path_to_datafile = r"C:\Users\jcris\OneDrive\Desktop\ENGR\315\Final Exam\wearable-dataset\subject-info.csv"

# first im gonna try and make sure that I can see the headers of the .csv file that has the subject information,
# so that we can parse through based on who does physical activity and what types of exercise they do.
df_subjectinfo = pd.read_csv(path_to_datafile)
# print(df_subjectinfo.head())
# that worked so now we can play around with the data...

# I have an idea to use dataframes instead of a for loop...
# The code below will create a variable for the active and inactive subjects and add the 'Info' column of the df_subjectinfo dataframe, if the 'Does physical activity regularly?',
# column starts with 'Yes'. We use the starts with argument because some of the columns are filled with 'Yes****' to indicate something happened with that test, but we still want,
# that to count as a yes. Then after we sort them all we are going to print each variable...
active_subjects = df_subjectinfo[
    df_subjectinfo['Does physical activity regularly?'].str.startswith('Yes')
]
exercise_yes = active_subjects['Info'].tolist()
print('Subjects who do exercise:', exercise_yes)

inactive_subjects = df_subjectinfo[
    df_subjectinfo['Does physical activity regularly?'].str.startswith('No')
]
exercise_no = inactive_subjects['Info'].tolist()
print('\nSubjects who do not exercise:', exercise_no)
print('\n')

# going to create a variable for all of the subjects identifiers...
all_subjects = exercise_yes + exercise_no

# ok so that worked, now we have two lists for each case of people. Now I want to make a variable to the aerobic folder...
path_to_AEROBIC = r"C:\Users\jcris\OneDrive\Desktop\ENGR\315\Final Exam\wearable-dataset\Wearable_Dataset\AEROBIC"

# I'm going to make a function first to grab all of the HR.csv data for each subject,
# then I'm going to have a seperate loop to do each analysis this time...
# the function below checks to see if the folder is called the subject_id, or subject_id_a, or subject_id_b because some of the data is listed like that and we don't want any bugs,
# then we will make an empty function for all_values. Then we will check every folder and try to find path_to_AEROBIC\subject_id, subject_id_a, and/or subject_id_b\HR.csv,
# the code will check to see if each of these exist, if any or all exist they will get put into the all_values variable for each subject, if they don't exist, the code does nothing.
# the function returns all_values...
def get_heartrate_data(subject_id):
    check_folder = [subject_id, subject_id + '_a', subject_id + '_b']
    all_values = []
    for folder in check_folder:
        heartrate_path = path_to_AEROBIC + '\\' + folder + '\\' + 'HR.csv'
        if os.path.exists(heartrate_path):
            heartrate_data = pd.read_csv(heartrate_path, header=0, skiprows=2)
            all_values.extend(heartrate_data.iloc[:, 0].tolist())
    return all_values if len(all_values) > 0 else None
# perfect, that should give us all of the values the heart rate data for each person saved as all_values.

# now we're going to find mu and std for each subject and plot one example normal distribution...
print(f"----- Normal Distribution -----")

# create an empty dictionary, or basically a bucket that we can fill with all the subject normal fit data...
subject_fits = {}

# now for every subject we're going to grab their heart rate data using the function we just made and save it as hr_values,
# if hr_values has substantial data and isnt full of practically nothing (a failsafe to avoid bugs), then fit it to a normal distribution,
# also add to the subject_fits dictionary for each subject a touple of mu, std, and hr_values which will be pulled later for the chi squared test.
# finally print out the results...
for subject in all_subjects:
    hr_values = get_heartrate_data(subject)
    if hr_values is not None and len(hr_values) > 1:
        mu, std = norm.fit(hr_values)
        subject_fits[subject] = (mu, std, hr_values)
        print(f"Subject {subject}: mu = {mu:.2f}, std = {std:.2f}")

# make two lists, one for the average heart rate for the group who exercises daily and one for the group who does not...
avg_hr_yes = []
avg_hr_no = []

# then were going to fill the two lists we just made with the average heart rate value of each subject, add to either list depending on if the subject is in,
# exercise_yes or exercise_no...
for subject, (mu, std, hr_values) in subject_fits.items():
    if subject in exercise_yes:
        avg_hr_yes.append(np.mean(hr_values))
    elif subject in exercise_no:
        avg_hr_no.append(np.mean(hr_values))

# take the average of each list above and save that to a list to compare for later...
overall_avg_yes = np.mean(avg_hr_yes)
overall_avg_no = np.mean(avg_hr_no)

# now I'm going to graph an example plot of the normal distribution for S01...
# start by making a variable for the example_subject and add to it the information from subject_fits for the first entry [0].
# then grab the nu, std, and hr data for the example_subject...
example_subject = list(subject_fits.keys())[0]
mu_ex, std_ex, hr_ex = subject_fits[example_subject]

# then build an x-axis for the plot that is 10 smaller than the smallest heart rate value, and 10 larger than the largest heart rate value, and have 300 points...
x = np.linspace(min(hr_ex) - 10, max(hr_ex) + 10, 300)

# assemble the plot
plt.figure(figsize=(10,5))
plt.plot(x, norm.pdf(x, mu_ex, std_ex), label=f'Subject {example_subject} Normal fit')
plt.xlabel('Heart Rate (bpm)')
plt.ylabel('Probability Density')
plt.title(f'Normal Distribution Fit - Subject {example_subject}')
plt.legend()
plt.tight_layout()
plt.savefig(f"normal_dist{example_subject}.png")
plt.show()
print(f"\n***Example plot saved for subject: {example_subject}***")

# now I'm going to conduct the chi squared test using alpha of 0.05, create a variable to count the number of good fits, and another variable to count the not good fits...
print(f"\n----- Chi Squared Goodness of Fit Test -----")
alpha = 0.05
good_fit_count = 0
not_fit_count = 0

# now for every subject with their mu, std, and heart rate values were going to turn the heart rate values into an array,
# then were going to create 9 bins from the minimum value of hr_array to the maximum value of hr_array,
# we're also going to add the negative and positive infinity bounds to the bins...
for subject, (mu, std, hr_values) in subject_fits.items():
    hr_array = np.array(hr_values)
    bins = np.linspace(hr_array.min(), hr_array.max(), 10)
    bins = np.concatenate([[-np.inf], bins, [np.inf]])

# then we're going to need to make a histogram of the actual distribution of hr_array with bins=bins we declared before,
# we also need the cdf_vals to find the expected distribution, to do that we use the norm.cdf function to find for each mu and std, what is the probability at each bin,
# then after we have cdf_vals we can find the expected distribution by taking the difference of cdf_vals times the length of the hr_array
    actual, _ = np.histogram(hr_array, bins=bins)
    cdf_vals = norm.cdf(bins, mu, std)
    expected = np.diff(cdf_vals) * len(hr_array)

# so up until this point we have no way of knowing if our expected data is actually usable, to find out if it is we are going to create a mask argument.
# we will start by making a True/False array the length of 'expected', and if the value of any bin is greater than 0.5 it goes in the True bin, and if it is less,
# than 0.5 it goes in the False bin. This will identify which bins are actually meaningful.
# then we have an if statement that counts the number of meaningful bins to make sure that more than two pass to ensure that there is enough data for a chi squared test...
    mask = expected > 0.5
    if mask.sum() < 2:
        print(f"Subject {subject}: Not enough data for chi2 test - skipping")
        continue

# the below variables weed out the insignificant bins so that we only have actual and expected values that passed the mask...
    actual_masked = actual[mask]
    expected_masked = expected[mask]

# the below line rescales the expected counts to match the actual total exactly, if we don't do this the chi squared test won't work...
    expected_masked = expected_masked * (actual_masked.sum() / expected_masked.sum())

# Now finally we can run the chi squared test and print out the results for each subject...
    chi2_stat, p_val = chisquare(actual_masked, f_exp=expected_masked)
    result = "GOOD FIT" if p_val > alpha else "NOT A GOOD FIT"
    print(f"Subject {subject}: chi2 = {chi2_stat:.2f}, p = {p_val:.5f} → {result}")

# below we will create the if statement to fill the variables good_fit_count and not_fit_count we created before, this will add 1 to either variable,
# every time there is a good fit or bad fit...
    if p_val > alpha:
        good_fit_count += 1
    elif p_val < alpha:
        not_fit_count += 1

# finally we will print the goodness of fit test conclusion based on the results from the counting above...
print(f"\n----- Goodness of Fit Conclusion -----")
print(f"Good fits: {good_fit_count:.2f} | Not a good fit: {not_fit_count:.2f}")
if good_fit_count == 0:
    print("Conclusion: No subjects had a heart rate that fit a normal distribution.")
    print("This imploes that heart rate during aerobic exercise is very low at some times, then climbs very high at others.")
elif not_fit_count == 0:
    print("Conclusion: All subjects had a heart rate that fit a normal distribution")

# finally, finally, we will answer Question 1 as it was posed, determining if the average heart rate during aerobic exercise was higher,
# for those who do physical activity often, or if it was higher for those who don't, and come to a conclusion based on those results...
print(f"\n----- Heart Rate Conclusion -----")
print(f"Subjects who exercise regularly: {overall_avg_yes:.2f} (bpm)")
print(f"Subjects who do not exercise regularly: {overall_avg_no:.2f} (bpm)")
if overall_avg_yes < overall_avg_no:
    print(f"Conclusion: If you do physical activity regularly, your HEART RATE WILL BE LOWER during Aerobic exercise than if you don't.")
elif overall_avg_yes > overall_avg_no:
    print(f"Conclusion: If you do physical activity regularly, your HEART WORKS HARDER during Aerobic exercise than if you don't.")

print(f"\n----- Question 4 -----")

avg_USweight_kg = 83.87
print(f"The Average weight for men and women in the U.S. is: {avg_USweight_kg} kg")

# we're going to sort the subjects based on if the value in the 'Weight (kg)' column is greater than the average '83.87', in which case that 'Info' column gets,
# added to the over_average variable, and if it is less than the average '83.87' then the 'Info' column gets added to under_average.
# then we print out each variable...
over_average = df_subjectinfo[
    df_subjectinfo['Weight (kg)'] > '83.87'
]
over_average_subjects = over_average['Info'].tolist()
print('\nSubjects Over Average Weight:', over_average_subjects)

under_average = df_subjectinfo[
    df_subjectinfo['Weight (kg)'] < '83.87'
]
under_average_subjects = under_average['Info'].tolist()
print('\nSubjects Under Average Weight:', under_average_subjects)

# now we're going to be using the heart rate data from the Anaerobic folder so give the filepath...
path_to_ANAEROBIC = r"C:\Users\jcris\OneDrive\Desktop\ENGR\315\Final Exam\wearable-dataset\Wearable_Dataset\ANAEROBIC"

# next we're going to create a function to find the average heartrate for each subject_id,
# the function below checks to see if the folder is called the subject_id, or subject_id_a, or subject_id_b because some of the data is listed like that and we don't want any bugs,
# then we will make an empty function for all_values. Then we will check every folder and try to find path_to_ANAEROBIC\subject_id, subject_id_a, and/or subject_id_b\HR.csv,
# the code will check to see if each of these exist, if any or all exist they will get put into the all_values variable for each subject, if they don't exist, the code does nothing.
# then the function will return the average of the all_values variable...
def get_avg_heartrate(subject_id):
    check_folder = [subject_id, subject_id + '_a', subject_id + 'b']
    all_values = []
    for folder in check_folder:
        heartrate_path = path_to_ANAEROBIC + '\\' + folder + '\\' + 'HR.csv'
        if os.path.exists(heartrate_path):
            heartrate_data = pd.read_csv(heartrate_path, header=0, skiprows=2)
            all_values.extend(heartrate_data.iloc[:, 0].tolist())
    if len(all_values) == 0:
        return None
    return(np.mean(all_values))

# now we're going to find the average heart rates of the over average subjects using a for loop,
# for each subject, have a variable called avg and fill that with the results of the function we just made for the subject,
# if that average is non-zero, add it to the hr_over_average_subjects variable...
hr_over_average_subjects = []
for subject in over_average_subjects:
    avg = get_avg_heartrate(subject)
    if avg is not None:
        hr_over_average_subjects.append(avg)

# then we're going to do the same thing for those who are under average weight in the U.S....
hr_under_average_subjects = []
for subject in under_average_subjects:
    avg = get_avg_heartrate(subject)
    if avg is not None:
        hr_under_average_subjects.append(avg)

# lastly, we are going to take the average of hr_over_average_subjects and hr_under_average_subjects so they can be compared...
final_average_hr_over = np.mean(hr_over_average_subjects)
final_average_hr_under = np.mean(hr_under_average_subjects)
print(f"\nAVG HR for Subjects Over Average: {final_average_hr_over}")
print(f"AVG HR for Subjects Under Average: {final_average_hr_under}")

# finally, we use a conditional to come to a conclusion based on the averages found above, these lines will provide the answer to the posed Question 4...
if final_average_hr_over > final_average_hr_under:
    print('\nConclusion: It appears that people who are OVER the average weight in the U.S. will have a higher heart rate during Anaerobic exercise compared to those UNDER the average weight.')

if final_average_hr_over < final_average_hr_under:
    print('\nConclusion: It appears that people who are UNDER the average weight in the U.S. will have a higher heart rate during Anaerobic exercise compared to those OVER the average weight.')

print(f"\n----- Question 5 -----")

ANAEROBIC_subjects = set(os.listdir(path_to_ANAEROBIC)) # get subjects in ANAEROBIC folder

AEROBIC_subjects = set(os.listdir(path_to_AEROBIC)) # get subjects in AEROBIC folder
subjects = sorted(ANAEROBIC_subjects & AEROBIC_subjects) # storing subjects that are in both anaerobic and aerobic folder

def c_to_f(celsius): #function converting data from degrees Celsius to degree Fahrenheit
    return (celsius * 9/5) + 32

def get_avg_skintemp_anaerobic(subject_id): # function to calculate average skin temperature for anaerobic exercise subjects
    check_folder = [subject_id, subject_id + '_a', subject_id + '_b']   # names of folders to ensure all subejct are accounted for

    all_values = [] # store all valid skin temperatures
    for folder in check_folder: # look through all folders
        skintemp_path = path_to_ANAEROBIC + '\\' + folder + '\\' 'TEMP.csv' # path to temperature data
        if os.path.exists(skintemp_path): # "if the path exists as given...""
            skintemp_anaerobic_data = pd.read_csv(skintemp_path, header=0, skiprows=2)  # read csv file
            temp_series = skintemp_anaerobic_data.iloc[:, 0] # column of temperature data
            #https://www.whoop.com/us/en/thelocker/what-is-skin-temperature-and-why-should-you-monitor-it/
            filtered_data = temp_series[(temp_series > 23) & (temp_series < 43)].tolist()   # filter data for temp values between 23-43 degrees Celsius
            all_values.extend(filtered_data) # all filtered data to a list
    if len(all_values) == 0: # "if all values is empty..."
        return None # "do nothing"
    return np.mean(all_values) # return average temperature



def get_avg_skintemp_aerobic(subject_id):   # function to calculate average skin temperature for aerobic exercise subjects
    check_folder = [subject_id, subject_id + '_a', subject_id + '_b']   # names of folders to ensure all subejct are accounted for

    all_values = [] # store all valid skin temperatures
    for folder in check_folder: # look through all folders
        skintemp_path = path_to_AEROBIC + '\\' + folder + '\\' 'TEMP.csv'   # path to temperature data
        if os.path.exists(skintemp_path):   # "if the path exists as given...""
            skintemp_aerobic_data = pd.read_csv(skintemp_path, header=0, skiprows=2)    # read csv file
            temp_series = skintemp_aerobic_data.iloc[:, 0]  # column of temperature data
            filtered_data = temp_series[(temp_series > 23) & (temp_series < 43)].tolist()   # filter data for temp values between 23-43 degrees Celsius
            all_values.extend(filtered_data)    # all filtered data to a list
    if len(all_values) == 0:    # "if all values is empty..."
        return None # "do nothing"
    return np.mean(all_values)  # return average temperature

# list to store average temperatures
anaerobic_avg = []
aerobic_avg = []
valid_subjects = []

for subject in subjects:
    ana = get_avg_skintemp_anaerobic(subject)   # average anaerobic data
    aer = get_avg_skintemp_aerobic(subject) # average aerobic data
    
    if ana is not None and aer is not None: # subjects with both datasets are kept
        anaerobic_avg.append(ana)
        aerobic_avg.append(aer)
        valid_subjects.append(subject)

anaerobic_avg_f = [c_to_f(temp) for temp in anaerobic_avg] # temperature conversion
aerobic_avg_f = [c_to_f(temp) for temp in aerobic_avg]

overall_anaerobic = np.mean(anaerobic_avg_f)    # overall average temperatures
overall_aerobic = np.mean(aerobic_avg_f)

print(f"Overall Anaerobic Exercise Skin Temperature: {overall_anaerobic:.2f} °F")   # print results
print(f"Overall Aerobic Exercise Skin Temperature: {overall_aerobic:.2f} °F")

if overall_anaerobic > overall_aerobic: # compare the coded information and return a result to indicate which form of exercise is better to make the body sweat
    print("\nConclusion: Anaerobic exercise produces higher skin temperature indicating more sweating which could indicate more body detoxification.")
elif overall_aerobic > overall_anaerobic:
    print("\nConclusion: Aerobic exercise produces higher skin temperature indicaitng more sweating which could indiicate more body detoxification.")
else:
    print("\nConclusion: Both are similar")


plt.figure(figsize=(12,6)) # plotting tools

plt.plot(valid_subjects, anaerobic_avg_f, marker='o', label='Anaerobic')
plt.plot(valid_subjects, aerobic_avg_f, marker='o', label='Aerobic')

plt.xlabel("Subject")
plt.ylabel("Average Skin Temperature (°F)")
plt.title("Anaerobic vs Aerobic Skin Temperature per Subject")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(f"skintemp_persubject.png")
plt.show()
print(f"\n***Plot Saved for Skin Temp***")
