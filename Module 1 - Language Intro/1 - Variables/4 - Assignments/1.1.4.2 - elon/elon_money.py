"""
This problem requires you to calculate compounding interest and final value of a  US treasury deposit based upon
current interest rates (that will be provided). Your analysis should return the final value of the investment
after a 10-year and 20-year period. The final values should be stored in the variables "ten_year_final"
and "twenty_year_final", respectively. Perform all your calculations in this file. Do not perform the calculations by hand
and simply write in the final result.

Prompt: On October 27th, 2022, Elon Musk purchased Twitter for $44B in total, with reportedly $33B of his own money. Since
that time, it appears this investment has not worked out. If Elon has instead bought $44B of US Treasury Bonds, how much
would his investment be worth in 10-year and 20-year bonds? Assume the 10-year bonds pay 3.96%,
the 20-year bonds pay 4.32%, with each compounding annually.
"""

### all your code below ###

import math

# A = P * math.pow((1 + (r/100)), n)

# define variables, P, r_10, r_20, n_1, n_2

P = 33000000000 # Elon's principal investment
r_10 = 3.96 # 10-year bond rate
r_20 = 4.32 # 20-year bond rate
n_1 = 10 # number of years for 10-year bond
n_2 = 20 # number of years for 20-year bond

# final answer for 10-year

ten_year_final = P * math.pow((1 + (r_10/100)), n_1)

# final answer for 20-year

twenty_year_final = P * math.pow((1 + (r_20/100)), n_2)

# print final answers

print("10-year final value: ", ten_year_final)

print("20-year final value: ", twenty_year_final)