#!/usr/bin/python3

import os
import sys
import argparse
import pdb

import random
import math


def gen_random_numbers(k):
    '''The prime number theorem assert that about one in ln n of the integers
    near n is a prime. Thus if we make 2ln n random choices, we will have high
    probability that one of our choices is a prime'''
    decimalVal = 2 ** k
    counts = math.ceil(2 * math.log(decimalVal))
    ran_list = []
    for c in range(counts):
        ran_a = random.getrandbits(k)
        ran_list.append(ran_a)

    return ran_list


def fermat_test(p):
    '''Fermat little theorem: if p is prime, then for any integer a,
    a^(p-1)=1 mod p'''
    ran_int = random.randint(1, p)
    test_num = ran_int ** (p-1)
    test_res = test_num % p
    if test_res == 1:
        return True
    else:
        return False


def miller_rabin_test(n, k=10):
    """ Miller-Rabin test for primality
    '''The miller-rabin primality test uses the following extension of Fermat little theorem:
            p is an odd prime number if and only if
            with p - 1 = 2^x * d, with d odd
            for every a coprime to p
        either a^d = 1 mod p, or there exists t such that 0 <= t < s and a^(2^t*d) = -1 mod p'''
    """
    if n == 2:
        return True
    if not n & 1:
        return False

    def check(a, s, d, n):
        x = pow(a, d, n)
        if x == 1:
            return True
        for i in range(s - 1):
            if x == n - 1:
                return True
            x = pow(x, 2, n)
        return x == n - 1

    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1

    for i in range(k):
        a = random.randrange(2, n - 1)
        print(a, " ")
        if not check(a, s, d, n):
            return False
        return True


def test_prime(num4test):
    '''The standard way to generate big prime numbers is to take a
    preselected random number of the desire length, apply a Fermat test
    and then to apply a certain number of Miller-Rabin tests (depending
    on the length and the allowed error rate like 2^-100) to get a number
    which is very probably a prime number'''
    if not fermat_test(num4test):
        return False

    if not miller_rabin_test(num4test):
        return False

    return True


def test_safe_prime(prime):
    '''a safe prime is a prime number of the form 2p+1,
    where p is also a prime'''
    test_num = (prime-1) / 2
    if test_prime(test_num):
        return True
    else:
        return False


def find_generator(n):
    '''math.gcd is available in newer version Python 3.5'''
    s = set(range(1, n))
    results = []
    for a in s:
        g = set()
        for x in s:
            g.add((a**x) % n)
        if g == s:
            results.append(a)
    rate = len(results) / (n-1)
    return rate, results


def get_primes(k):
    '''
    For generate prime numbers in a range, we can generate random numbers
    within the appropriate range and quickly test them for primality

    The prime number theorem asserts that about one in ln n of the integers
    near n is a prime. Thus, if we make 2ln n random choices, we will have
    high probility that one of our choices is a prime
    '''
    # gen random k-bit number list
    ran_list = gen_random_numbers(k)
    #print('get random number list: {}'.format(ran_list))

    # test the number if they are prime
    prime_list = []
    for ran_num in ran_list:
        if test_prime(ran_num):
            prime_list.append(ran_num)

    ran_len = len(ran_list)
    rate = len(prime_list) / ran_len
    return rate, prime_list, ran_len


def get_safe_primes(k):
    '''a safe prime is a prime number of the form 2p+1, where p is also a prime'''
    tmp_rate, prime_list, ran_len = get_primes(k)

    safe_prime_list = []
    for prime in prime_list:
        if test_safe_prime(prime):
            safe_prime_list.append(prime)

    rate = len(safe_prime_list) / ran_len
    return rate, safe_prime_list


def get_generators_for_primes(k):
    '''a generator of a group G is an element whose powers comprise the entire
    group G. If a group has a generator, then it is a cyclic group'''
    _, safe_prime_list = get_safe_primes(k)
    generator_list = []
    for s_prime in safe_prime_list:
        generator = find_generator(s_prime)
        generator_list.append(generator)

    return generator_list


def run(k, opts):
    '''
    for each k = 16, 128, 256, 512, 768, 1024 determine the rate of success using random
    choices of k-bit numbers:
    a) emitting prime numbers
    b) emitting safe-prime numbers
    c) emitting generators for each prime emitted in b)
    NB: In python, it is easy to generate a random number with k bits: rand_a = random.getrandbits(k)
    '''
    if 'prime' == opts.method:
        # emitting prime numbers
        rate, prime_list, _ = get_primes(k)
        print('emitting rate of prime for {} bit data is: {:f}'.format(k, rate))
    elif 'safe_prime' == opts.method:
        # emitting safe-prime numbers
        rate, safe_prime_list = get_safe_primes(k)
        print('emitting rate of safe prime for {} bit data is: {:f}'.format(k, rate))
    elif 'generator' == opts.method:
        # emitting generators for each prime emitted in b)
        rate, generator_list = get_generators_for_primes(k)
        print('emitting rate of generator for {} bit data is: {:f}'.format(k, rate))
    else:
        raise NotImplementedError()


def main(opts):
    #k_list = [16, 128, 256, 512, 768, 1024]
    k_list = [16, 8]
    for k in k_list:
        run(k, opts)

    print('all test done!')


def parseArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--method',
                        help='choose from prime/safe_prime/generator')
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    opts = parseArgs(sys.argv)
    main(opts)
