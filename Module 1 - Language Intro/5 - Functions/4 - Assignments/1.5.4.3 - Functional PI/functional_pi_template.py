import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """

    ### YOUR CODE HERE ###
    a = 1.0
    b = 1.0 / math.sqrt(2.0)
    t = 0.25
    p = 1.0
    for i in range(1, 10):
        y = (a + b) / 2.0
        z = math.sqrt(a * b)
        t = t - p * (a - y) ** 2
        a = y
        b = z
        p = 2.0 * p
        pi_estimate = (a + b) ** 2 / (4 * t)
    # change this so an actual value is returned
    return pi_estimate




desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
