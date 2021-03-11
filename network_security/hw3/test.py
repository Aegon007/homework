# -*- coding: utf-8 -*-
#!/usr/bin/env python

## EstimatingExponentFromExecutionTime.py

##  Avi Kak (kak@purdue.edu)
##  March 31, 2015

## This script demonstrates the basic idea of how it is possible to infer
##  the bit field of an exponent by measuring the time it takes to carry
##  out the one of the key steps in the modular exponentiation algorithm

import time

## This is from
## Lecture 32 of Dr. Avi Kak (kak@purdue.edu):
def modular_exponentiate(A, B, modulus):
    time_trace = []
    result = 1
    while B > 0:
        start = time.time()
        if B & 1:
            result = ( result * A ) % modulus
        elapsed = time.time() - start
        time_trace.append(elapsed)
        B = B >> 1
        A = ( A * A ) % modulus
    return result, time_trace

## Since a single experiment does not yield reliable measurements of the time
## taken by a computational step, this function helps us carry out repeated
## experiments:

def repeated_time_measurements(A, B, modulus, how_many_times):
    list_of_time_traces = []
    results = []
    for i in range(how_many_times):
        result, timetrace = modular_exponentiate(A, B, modulus)
        list_of_time_traces.append(timetrace)
        results.append(result)
    return list_of_time_traces, results

A= 123456789012345678901234567890123456789012345678901234567890
B = 0b1111110101001001
modulus = 987654321
num_iterations = 100
print "\nnum_iterations = ", num_iterations

list_of_time_traces, results = repeated_time_measurements(A, B, modulus, num_iterations)

sums = [sum(e) for e in zip(*list_of_time_traces)]
averages = [x/num_iterations for x in sums]
averages = list(reversed(averages))
## print "\ntimings: ", averages
minval, maxval = min(averages), max(averages)
threshold = (maxval - minval) / 2
bitstring = ''
for item in averages:
    if item > threshold:
        bitstring += "1"
    else:
        bitstring += "0"
print "\n bitstring for B constructed from timings: ", bitstring
print "\n the real value of B in this experiment: ", bin(B)
