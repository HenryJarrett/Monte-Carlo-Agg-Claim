import random

def factorial(x):
    if x == 1 or x == 0:
        return 1
    return x*factorial(x-1)

def exponential(x):
    return 2.718281828**x

def ln(x):
    # Assert that x is in the correct domain
    if x < 0:
        raise Exception("Domain Error")

    # Find a rough guess for ln(x) 
    xi = 0
    while (exponential(xi-1) > x) or (exponential(xi) < x):
        if x > 1:
            xi += 1
        else:
            xi -= 1

    # Apply newtons method to find ln(x)
    dif = exponential(xi)-x
    while dif > 0.0000000001 or dif < -0.0000000001:
        # Update xi to the next guess
        xi = xi - (exponential(xi) - x)/(exponential(xi))
        # Calculate the new difference
        dif = exponential(xi)-x
    return xi

# Generate a random value between 0 and 1
def uniformGen():
    val = min(0.999, round(random.random(), 3))
    return max(val, 0.001)
