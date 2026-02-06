import random

"""
THIS SECTION IS DR. FORSYTH'S CODE. DO NOT MODIFY. BUT KEEP READING.
"""

# randomly sample a distribution between 2 and 6
random_number = int(random.uniform(2, 6))

# any number times 2 is even
an_odd_number = 2 * random_number

# generate a random list of odd length containing values up to 100
even_list = random.sample(range(100), an_odd_number)

# print out the list contents
print("Your list is: ", even_list)

"""
YOUR CODE BEGINS BELOW HERE. FILL IN THE MISSING OPERATIONS / CODE
"""

length_even_list = len(even_list)

print("The Length of the list is:", length_even_list)

middle_index = length_even_list // 2

# this is the final result. Modify this line, and the empty lines above, to solve the assignment
middle_average = (even_list[middle_index - 1] + even_list[middle_index]) / 2

# the average of middle elements is
print("The average is: ", middle_average)
