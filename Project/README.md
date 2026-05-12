**ENGR 315 Final Project: Wearable Dataset - Austin Conley, Justin Criscuolo, Paul Clossey**

*Project Description*
- The goal of this project was to analyze a selected dataset by developing a python algorithm.
- The team needed to identify potential questions that were answerable given the data in the selected set.
- The team then had to down-select from 5 questions, to just 3. The answers to which the algorithm was meant to find.
   - The questions ultimately selected are:
      - #1: "On average, how do the heart rates of participants who reportedly do physical activity often,
        compare to participants who don't do physical activity often; during aerobic exercise?"
      - #2: (Denoted as Question 4... reference the .pdf file in this folder) "For individuals over the average weight in the U.S.,
        how does anaerobic exercise affect heart rate compared to those under the average?"
      - #3: (Denoted as Question 5... reference .pdf file) "Do anaerobic exercise or aerobic exercises
        increase skin temperature more?"

**Link To Dataset**
- https://physionet.org/content/wearable-device-dataset/1.0.1/
   - *Dataset Description*
   - A description of the dataset above can be found by following the provided link, however, in summary:
      - This dataset was originally collected to study stress induction, as a group of men and women of different ages
        participated in physical activities (aerobic and anaerobic). This data was recorded using the Empatica E4, a research wearable.
      - As previously stated, learning about how stress manifests itself during different activities was the orignial goal of this dataset,
        but the majority of the data collected is applicable to other fields of study.
      - For example, the collected data that is present in the set for every individual subject includes Heart Rate (HR.csv), Skin Temperature
        (TEMP.csv), Electrodermal Activity (EDA.csv), Photoplethysmograph data (BVP.csv), Accelerometer data (ACC.csv), and time between heart beats in the BVP.csv file (IBI.csv).
      - For the questions stated above, the data that used will only come from: HR.csv and TEMP.csv.
      - In addition to the data mentioned above, there was a master-file called subject-info.csv. This file contains demographic data for each
        participant, which the team used to sort the participants into groups based on the question criteria.
- **Important Note**: The filepaths in our algorithm are hard coded to our machines based on where we downloaded the dataset to, and will need to
 be updated. The path variables are; path_to_datafile (subject-info.csv (line 10)), path_to_AEROBIC (line 39), and path_to_ANAEROBIC (line 200).

*Library Requirements*
- The libraries for the functions used in the algorithm are as follows:
   - import pandas as pd
   - import numpy as np
   - import matplotlib.pyplot as plt
   - import os
   - from scipy.stats import norm, chisquare
   - import math

*How To Run*
- Open and run "Combined Proposal Questions.py" after changing the filepaths. Each Question is labeled in the code and also in the output,
  and the code should run top-to-bottom.
- Figures are set to be saved in the "Project" folder

*Project Results Summary*
- #1: Question 1 will first print out the list of subjects who do and do not exercise, then the Normal Distributions (mu and std) will be printed
  for all subjects. An example plot will be generated, showing the Normal Distribution for one subject. Then the Chi Squared Goodness of Fit Test
  will print with a conclusion drawn from the results. Lastly, the main conclusion for the question will be printed.
- #2: Question 4 will first print out the average weight for men and women that was used for the analysis. Then the list of subjects over and
  under that average will be printed. Then the average heart rate for the over and under groups will be printed, and finally the conclusion for
  the question will print.
- #3: For the final question, Question 3, the skin temperature plot for each subject will plot, then the overall skin temperatures for both types
  of exercise will print. Then the Question 3 conclusion will print.