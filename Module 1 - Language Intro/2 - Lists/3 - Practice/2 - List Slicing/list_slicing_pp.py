# this is practice on slicing arrays in Python.
# slicing arrays is using the index to "slice" certain parts
# of a list.
# it relies on the use of a colon, and the indexes of the list.

list = [5, 10, 15, 20, 25, 30]
example_list = ["red", "blue", "yellow", "green", "orange"]

# to select the entire array, use just the colon, like so:
colors = example_list[:]
print("Colors in example_list: " + str(colors))

# now, you try: store all of "list" in the variable "numbers"
numbers = list[:]
print("Numbers in list: " + str(numbers))


# next, you can select everything from a certain index onward to the
# end of the list
favorites = example_list[3:]
print("Favorite colors: " + str(favorites))

# your turn: select the last 4 elements of list
over_10 = list[-4:]
print("Numbers over 10: " + str(over_10))


# by moving the integer to behind the colon, you can select everything up
# to a certain index in the list
primary_colors = example_list[:2]
print("All primary colors: " + str(primary_colors))

# store all the numbers less than 20 in "list" using this method and
# store it in the variable below
under_20 = list[:3]
print("Numbers under 20: " + str(under_20))


# you can also choose to select from one index up until another index
# the -1 index means up until the last element
names_list = ["Frank", "Sally", "Grant", "Amelia", "Ricardo", "Rachelle"]
friends = names_list[2:-1]
print("My friends: " + str(friends))

# now, select the two numbers in the middle of "list"
median = list[2:-2]
print(median)
