"""
Problem 2:

Calculate the sum of all even Fibonacci numbers below positive integer n

Example:
>>> sum_even_fibs_under_n(10)
10

This file also includes a function that returns the nth Fibonacci number:
>>> fib(0)
1

>>> fib(1)
1

>>> fib(10)
89


Author: Jessica Yung
Refactored October 2016
"""


def fib(n):
    """Function to calculate nth Fibonacci number, n being a non-negative integer.
    Def: 0th Fibonacci number is 1.
    """
    if n < 0:
        return "Null"
    elif n == 0 or n == 1:
        return 1
    else:
        f_two_before = 1
        f = 1
        for i in range(2, n+1):
            # Save the value of f for use later
            f_save = f
            f = f + f_two_before
            # Additional print statement for clarity            
            # print(i, "th Fib is ", f)
            f_two_before = f_save
        return f
  

def sum_even_fibs_under_n(n):
    """Calculates sum of even Fibonacci numbers under n."""
    if fib(2) < n:    
        sum = 0    
        i = 2    
        while fib(i) < n:
            sum += fib(i)
            i += 3
        return sum
    else:
        return "Null"
