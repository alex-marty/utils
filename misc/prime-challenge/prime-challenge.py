# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 12:48:49 2016

@author: amarty

Challenge: Find the probability for a prime number ending by 9 to be
followed by a prime ending by 1 / 3 / 7 / 9. Only consider here numbers lesser
than 25*10^6.
"""

import numpy as np


def is_prime(n):
    """ Returns whether n is a prime or not """
    if n == 0 or n == 1:
        return False
    for d in range(2, int(np.ceil(np.sqrt(n))) + 1):
        if n % d == 0:
            return False
    return True


def get_primes(max_n, print_progress=False):
    """ Returns the list of primes lesser than or equal to max_n """
    primes = []    
    for n in range(max_n + 1):
        if print_progress and n % int(max_n / 100) == 0:
            print("n={}, len(primes)={}".format(n, len(primes)), flush=True)
        if is_prime(n):
            primes.append(n)
    return primes


def last_digit(n):
    return n % 10


def get_next_distribution(primes, digit=9):
    """ Returns the number of occurrences of primes with every last digit,
    following primes ending with a given digit.
    """
    dist = [0] * 10
    for i in range(len(primes)):
        p = primes[i]
        if last_digit(p) == digit:
            dist[last_digit(primes[i+1])] += 1
    return dist


if __name__ == "__main__":
    PRIMES_PATH = "W:\\workspace\\prime-challenge\\primes_lt_25M.csv"
    primes = []
    with open(PRIMES_PATH, "r") as primes_file:
        primes = [int(r.strip()) for r in primes_file]
    next_primes_9 = [n for n in primes if last_digit(n) == 9]
    dist = get_next_distribution(primes, 9)
    probs = [n / len(next_primes_9) for n in dist]
    print(probs)
