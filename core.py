# Mathematical functions and computation logic
# All trigonometric functions work in radians

PI = 3.14159265358979323846

# Basic operations
def addition(a, b):
    return a + b

def subtraction(a, b):
    return a - b

def multiplication(a, b):
    return a * b

def division(a, b):
    if b == 0:
        return "Error: division by zero"
    return a / b

def power(base, exponent):
    if exponent == 0:
        return 1
    if exponent == int(exponent):
        result = 1
        for i in range(abs(int(exponent))):
            result *= base
        return 1 / result if exponent < 0 else result
    return base ** exponent

# Roots and factorial
def square_root(n):
    if n < 0:
        return "Error: negative number"
    if n == 0:
        return 0
    return power(n, 0.5)

def cube_root(n):
    if n == 0:
        return 0
    if n < 0:
        return -power(-n, 1/3)
    return power(n, 1/3)

def factorial(n):
    if n < 0:
        return "Error: negative number"
    if n != int(n):
        return "Error: integer required"
    n = int(n)
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Trigonometry (Taylor series implementation)
def cosine(x, terms=15):
    # Normalize x to [-pi, pi]
    while x > PI:
        x -= 2 * PI
    while x < -PI:
        x += 2 * PI
    result = 0
    for n in range(terms):
        sign = power(-1, n)
        numerator = power(x, 2 * n)
        denominator = factorial(2 * n)
        result += sign * numerator / denominator
    return result

def sine(x, terms=15):
    # Normalize x to [-pi, pi]
    while x > PI:
        x -= 2 * PI
    while x < -PI:
        x += 2 * PI
    result = 0
    for n in range(terms):
        sign = power(-1, n)
        numerator = power(x, 2 * n + 1)
        denominator = factorial(2 * n + 1)
        result += sign * numerator / denominator
    return result

def tangent(x):
    c = cosine(x)
    if abs(c) < 1e-10:
        return "Tangent undefined at this value"
    return sine(x) / c

# Equation solvers
def first_degree_equation(a, b):
    # ax + b = 0
    if a == 0 and b == 0:
        return "Infinite solutions"
    if a == 0:
        return "No solution"
    return -b / a

def second_degree_equation(a, b, c):
    # ax^2 + bx + c = 0
    if a == 0:
        return "Error: not quadratic"
    delta = b * b - 4 * a * c
    if delta > 0:
        d = square_root(delta)
        x1 = (-b - d) / (2 * a)
        x2 = (-b + d) / (2 * a)
        return (x1, x2)
    if delta == 0:
        x = -b / (2 * a)
        return (x,)
    return "No real solution"

# Utilities
def absolute_value(n):
    if n < 0:
        return -n
    return n

def modulo(a, b):
    if b == 0:
        return "Error: division by zero"
    return a - (int(a / b) * b)

def degrees_to_radians(degrees):
    return degrees * PI / 180

def get_pi():
    return PI

# Result formatting (max 6 decimals, no trailing zeros)
def format_result(value):
    if isinstance(value, str):
        return value
    if isinstance(value, int):
        return str(value)
    if value == int(value):
        return str(int(value))
    formatted = f"{value:.6f}"
    formatted = formatted.rstrip('0').rstrip('.')
    return formatted
