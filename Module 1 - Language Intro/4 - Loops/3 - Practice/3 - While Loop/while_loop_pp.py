# this will test your ability to write a while loop
# use the print() statement to determine whether your number is correct

# an example while loop is given below
a = 1
while a != 5:
    print("not 5 yet, but we're at " + str(a))
    a = a + 1  # pay attention where the counter (this part of the loop) is located
    

# now, move the counter to after the print statement
# notice how the value of a has changed in the print value,
# but remains the same in the actual value of a

# first, we're going to write the condition of a while loop
# this loop is going to multiply the variable b by 2 3 times
b = 5
x = 0
while x < 3:
    print("b is currently " + str(b))
    b = b * 2
    x = x + 1

# now, try and write the body of a while loop that should add a variable to itself 5 times
# when writing the code delete "break" - this is to prevent an infinite loop
c = 3
y = 0
while y < 5:
    c = c + c
    y = y + 1

# it's time to combine both of these concepts.
# write a loop entirely from scratch that prints out a statement 6 times
# the counter variable you will use is z
z = 1
while z < 7:
    print("this is the " + str(z) + " time a statement has been printed ")
    z = z + 1