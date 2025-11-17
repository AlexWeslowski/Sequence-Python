import sys, os, multiprocessing, multiprocessing.managers, math, sympy, numba, itertools, functools, operator, primefac, fractions, bitarray, time
import win32api, win32process, win32con
import divisors as div
from fractions import Fraction
from multiprocessing import Process, Queue
from queue import Empty
from filelock import Timeout, FileLock

# try:
#    import pyjion
# except:
#    pass

# 2**28 ~ 10**8.43
# 2**29 = 536,870,912
# 2**33 ~ 10**9.93
arysequence = bitarray.bitarray(2**10)
arysequence.setall(0)
aryprimes = bitarray.bitarray(2**10)
aryprimes.setall(0)
try:
    import primesieve
    for p in primesieve.primes(2**10):
        aryprimes[p] = 1
except ModuleNotFoundError as mnfe:
    for p in sympy.sieve.primerange(2**10):
        aryprimes[p] = 1
    pass

# setfractions = frozenset([Fraction(1, 2),])
setfractions = frozenset([Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5),])
n = 0
combinations = []
max_sum = 0.5
min_factors = 2
max_factors = 10
directory_path = os.path.dirname(os.path.abspath(sys.argv[0]))
file_path = f"{directory_path}\\sequence_pr.txt"


class Sequence(object):
    # setfractions, aryprimes, arysequence, t0, i0, i1, i2
    def __init__(self, sfractions, aprimes, asequence, t0, i0, i1, i2):
        self.t0 = t0
        self.i0 = i0
        self.i1 = i1
        self.i2 = i2
        self.bbreak = False
        self.setfractions = sfractions
        self.aryprimes = aprimes
        self.arysequence = asequence
        self.verbose = False
        self.min_factors = 2
        self.max_factors = 10
 
    def mult(self, tpl):
        ary = list(tpl)
        if True:
            ilen = len(ary)
            # ary[1] = ary[0]*ary[1] if self.aryprimes[ary[0]] or self.aryprimes[ary[1]] else ary[0]*ary[1]//math.gcd(ary[0], ary[1])
            ary[1] = ary[0]*ary[1] if self.aryprimes[ary[0]] or self.aryprimes[ary[1]] else math.lcm(ary[0], ary[1])
            if ilen <= 2:
                return ary[1]
            else:
                for a in range(2, 10 + 1):
                    # ary[a] = ary[a - 1]*ary[a] if self.aryprimes[ary[a]] else ary[a - 1]*ary[a]//math.gcd(ary[a - 1], ary[a])
                    ary[a] = ary[a - 1]*ary[a] if self.aryprimes[ary[a]] else math.lcm(ary[a - 1], ary[a])
                    if ilen <= a + 1:
                        return ary[a]
    
    def calc_density(self, i, a):
        global max_sum
        bcheck = False
        ilen = len(a)
        sum = Fraction(1, a[0])
        if bcheck and sum > max_sum:
            return Fraction(1, 1)
        sum += Fraction(1, a[1]) - Fraction(1, self.mult(tuple(a[0:2])))
        if bcheck and sum > max_sum:
            return 1.0
        if ilen >= 3:
            sum += Fraction(1, a[2]) - Fraction(1, self.mult((a[0], a[2]))) - Fraction(1, self.mult((a[1], a[2]))) + Fraction(1, self.mult(tuple(a[0:3])))
            if bcheck and sum > max_sum:
                return Fraction(1, 1)
        if ilen >= 4:
            sum += Fraction(1, a[3]) - Fraction(1, self.mult((a[0], a[3]))) - Fraction(1, self.mult((a[1], a[3]))) - Fraction(1, self.mult((a[2], a[3]))) + Fraction(1, self.mult((a[0], a[1], a[3]))) + Fraction(1, self.mult((a[0], a[2], a[3]))) + Fraction(1, self.mult((a[1], a[2], a[3]))) - Fraction(1, self.mult(tuple(a[0:4])))
            if bcheck and sum > max_sum:
                return Fraction(1, 1)
        if ilen >= 5:
            sum += Fraction(1, a[4]) - Fraction(1, self.mult((a[0], a[4]))) - Fraction(1, self.mult((a[1], a[4]))) - Fraction(1, self.mult((a[2], a[4]))) - Fraction(1, self.mult((a[3], a[4]))) + Fraction(1, self.mult((a[0], a[1], a[4]))) + Fraction(1, self.mult((a[0], a[2], a[4]))) + Fraction(1, self.mult((a[0], a[3], a[4]))) + Fraction(1, self.mult((a[1], a[2], a[4]))) + Fraction(1, self.mult((a[1], a[3], a[4]))) + Fraction(1, self.mult((a[2], a[3], a[4]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[4]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[4]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[4]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[4]))) + Fraction(1, self.mult(tuple(a[0:5])))
            if bcheck and sum > max_sum:
                return Fraction(1, 1)
        if ilen >= 6:
            sum += Fraction(1, a[5]) - Fraction(1, self.mult((a[0], a[5]))) - Fraction(1, self.mult((a[1], a[5]))) - Fraction(1, self.mult((a[2], a[5]))) - Fraction(1, self.mult((a[3], a[5]))) - Fraction(1, self.mult((a[4], a[5]))) + Fraction(1, self.mult((a[0], a[1], a[5]))) + Fraction(1, self.mult((a[0], a[2], a[5]))) + Fraction(1, self.mult((a[0], a[3], a[5]))) + Fraction(1, self.mult((a[0], a[4], a[5]))) + Fraction(1, self.mult((a[1], a[2], a[5]))) + Fraction(1, self.mult((a[1], a[3], a[5]))) + Fraction(1, self.mult((a[1], a[4], a[5]))) + Fraction(1, self.mult((a[2], a[3], a[5]))) + Fraction(1, self.mult((a[2], a[4], a[5]))) + Fraction(1, self.mult((a[3], a[4], a[5]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[5]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[5]))) - Fraction(1, self.mult((a[0], a[1], a[4], a[5]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[5]))) - Fraction(1, self.mult((a[0], a[2], a[4], a[5]))) - Fraction(1, self.mult((a[0], a[3], a[4], a[5]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[5]))) - Fraction(1, self.mult((a[1], a[2], a[4], a[5]))) - Fraction(1, self.mult((a[1], a[3], a[4], a[5]))) - Fraction(1, self.mult((a[2], a[3], a[4], a[5]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[5]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[5]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[5]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[5]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[5]))) - Fraction(1, self.mult(tuple(a[0:6])))
            if bcheck and sum > max_sum:
                return Fraction(1, 1)
        if ilen >= 7:
            sum += Fraction(1, a[6]) - Fraction(1, self.mult((a[0], a[6]))) - Fraction(1, self.mult((a[1], a[6]))) - Fraction(1, self.mult((a[2], a[6]))) - Fraction(1, self.mult((a[3], a[6]))) - Fraction(1, self.mult((a[4], a[6]))) - Fraction(1, self.mult((a[5], a[6]))) + Fraction(1, self.mult((a[0], a[1], a[6]))) + Fraction(1, self.mult((a[0], a[2], a[6]))) + Fraction(1, self.mult((a[0], a[3], a[6]))) + Fraction(1, self.mult((a[0], a[4], a[6]))) + Fraction(1, self.mult((a[0], a[5], a[6]))) + Fraction(1, self.mult((a[1], a[2], a[6]))) + Fraction(1, self.mult((a[1], a[3], a[6]))) + Fraction(1, self.mult((a[1], a[4], a[6]))) + Fraction(1, self.mult((a[1], a[5], a[6]))) + Fraction(1, self.mult((a[2], a[3], a[6]))) + Fraction(1, self.mult((a[2], a[4], a[6]))) + Fraction(1, self.mult((a[2], a[5], a[6]))) + Fraction(1, self.mult((a[3], a[4], a[6]))) + Fraction(1, self.mult((a[3], a[5], a[6]))) + Fraction(1, self.mult((a[4], a[5], a[6]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[6]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[6]))) - Fraction(1, self.mult((a[0], a[1], a[4], a[6]))) - Fraction(1, self.mult((a[0], a[1], a[5], a[6]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[6]))) - Fraction(1, self.mult((a[0], a[2], a[4], a[6]))) - Fraction(1, self.mult((a[0], a[2], a[5], a[6]))) - Fraction(1, self.mult((a[0], a[3], a[4], a[6]))) - Fraction(1, self.mult((a[0], a[3], a[5], a[6]))) - Fraction(1, self.mult((a[0], a[4], a[5], a[6]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[6]))) - Fraction(1, self.mult((a[1], a[2], a[4], a[6]))) - Fraction(1, self.mult((a[1], a[2], a[5], a[6]))) - Fraction(1, self.mult((a[1], a[3], a[4], a[6]))) - Fraction(1, self.mult((a[1], a[3], a[5], a[6]))) - Fraction(1, self.mult((a[1], a[4], a[5], a[6]))) - Fraction(1, self.mult((a[2], a[3], a[4], a[6]))) - Fraction(1, self.mult((a[2], a[3], a[5], a[6]))) - Fraction(1, self.mult((a[2], a[4], a[5], a[6]))) - Fraction(1, self.mult((a[3], a[4], a[5], a[6]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[6]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[6]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[5], a[6]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[6]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[5], a[6]))) + Fraction(1, self.mult((a[0], a[1], a[4], a[5], a[6]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[6]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[5], a[6]))) + Fraction(1, self.mult((a[0], a[2], a[4], a[5], a[6]))) + Fraction(1, self.mult((a[0], a[3], a[4], a[5], a[6]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[6]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[5], a[6]))) + Fraction(1, self.mult((a[1], a[2], a[4], a[5], a[6]))) + Fraction(1, self.mult((a[1], a[3], a[4], a[5], a[6]))) + Fraction(1, self.mult((a[2], a[3], a[4], a[5], a[6]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[4], a[6]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[5], a[6]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[5], a[6]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[5], a[6]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[5], a[6]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[5], a[6]))) + Fraction(1, self.mult(tuple(a[0:7])))
            if bcheck and sum > max_sum:
                return Fraction(1, 1)
        if ilen >= 8:
            sum += Fraction(1, a[7]) - Fraction(1, self.mult((a[0], a[7]))) - Fraction(1, self.mult((a[1], a[7]))) - Fraction(1, self.mult((a[2], a[7]))) - Fraction(1, self.mult((a[3], a[7]))) - Fraction(1, self.mult((a[4], a[7]))) - Fraction(1, self.mult((a[5], a[7]))) - Fraction(1, self.mult((a[6], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[7]))) + Fraction(1, self.mult((a[0], a[2], a[7]))) + Fraction(1, self.mult((a[0], a[3], a[7]))) + Fraction(1, self.mult((a[0], a[4], a[7]))) + Fraction(1, self.mult((a[0], a[5], a[7]))) + Fraction(1, self.mult((a[0], a[6], a[7]))) + Fraction(1, self.mult((a[1], a[2], a[7]))) + Fraction(1, self.mult((a[1], a[3], a[7]))) + Fraction(1, self.mult((a[1], a[4], a[7]))) + Fraction(1, self.mult((a[1], a[5], a[7]))) + Fraction(1, self.mult((a[1], a[6], a[7]))) + Fraction(1, self.mult((a[2], a[3], a[7]))) + Fraction(1, self.mult((a[2], a[4], a[7]))) + Fraction(1, self.mult((a[2], a[5], a[7]))) + Fraction(1, self.mult((a[2], a[6], a[7]))) + Fraction(1, self.mult((a[3], a[4], a[7]))) + Fraction(1, self.mult((a[3], a[5], a[7]))) + Fraction(1, self.mult((a[3], a[6], a[7]))) + Fraction(1, self.mult((a[4], a[5], a[7]))) + Fraction(1, self.mult((a[4], a[6], a[7]))) + Fraction(1, self.mult((a[5], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[4], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[5], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[7]))) - Fraction(1, self.mult((a[0], a[2], a[4], a[7]))) - Fraction(1, self.mult((a[0], a[2], a[5], a[7]))) - Fraction(1, self.mult((a[0], a[2], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[3], a[4], a[7]))) - Fraction(1, self.mult((a[0], a[3], a[5], a[7]))) - Fraction(1, self.mult((a[0], a[3], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[4], a[5], a[7]))) - Fraction(1, self.mult((a[0], a[4], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[5], a[6], a[7]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[7]))) - Fraction(1, self.mult((a[1], a[2], a[4], a[7]))) - Fraction(1, self.mult((a[1], a[2], a[5], a[7]))) - Fraction(1, self.mult((a[1], a[2], a[6], a[7]))) - Fraction(1, self.mult((a[1], a[3], a[4], a[7]))) - Fraction(1, self.mult((a[1], a[3], a[5], a[7]))) - Fraction(1, self.mult((a[1], a[3], a[6], a[7]))) - Fraction(1, self.mult((a[1], a[4], a[5], a[7]))) - Fraction(1, self.mult((a[1], a[4], a[6], a[7]))) - Fraction(1, self.mult((a[1], a[5], a[6], a[7]))) - Fraction(1, self.mult((a[2], a[3], a[4], a[7]))) - Fraction(1, self.mult((a[2], a[3], a[5], a[7]))) - Fraction(1, self.mult((a[2], a[3], a[6], a[7]))) - Fraction(1, self.mult((a[2], a[4], a[5], a[7]))) - Fraction(1, self.mult((a[2], a[4], a[6], a[7]))) - Fraction(1, self.mult((a[2], a[5], a[6], a[7]))) - Fraction(1, self.mult((a[3], a[4], a[5], a[7]))) - Fraction(1, self.mult((a[3], a[4], a[6], a[7]))) - Fraction(1, self.mult((a[3], a[5], a[6], a[7]))) - Fraction(1, self.mult((a[4], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[5], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[5], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[4], a[5], a[7])))
            sum += Fraction(1, self.mult((a[0], a[1], a[4], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[7]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[5], a[7]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[2], a[4], a[5], a[7]))) + Fraction(1, self.mult((a[0], a[2], a[4], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[2], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[3], a[4], a[5], a[7]))) + Fraction(1, self.mult((a[0], a[3], a[4], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[3], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[4], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[7]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[5], a[7]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[6], a[7]))) + Fraction(1, self.mult((a[1], a[2], a[4], a[5], a[7]))) + Fraction(1, self.mult((a[1], a[2], a[4], a[6], a[7]))) + Fraction(1, self.mult((a[1], a[2], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[1], a[3], a[4], a[5], a[7]))) + Fraction(1, self.mult((a[1], a[3], a[4], a[6], a[7]))) + Fraction(1, self.mult((a[1], a[3], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[1], a[4], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[2], a[3], a[4], a[5], a[7]))) + Fraction(1, self.mult((a[2], a[3], a[4], a[6], a[7]))) + Fraction(1, self.mult((a[2], a[3], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[2], a[4], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[4], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[5], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[5], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[5], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[5], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[5], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[1], a[4], a[5], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[5], a[7]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[5], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[2], a[4], a[5], a[6], a[7]))) - Fraction(1, self.mult((a[0], a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[5], a[7]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[6], a[7]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[5], a[6], a[7]))) - Fraction(1, self.mult((a[1], a[2], a[4], a[5], a[6], a[7]))) - Fraction(1, self.mult((a[1], a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, self.mult((a[2], a[3], a[4], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[4], a[5], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[4], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[5], a[6], a[7]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, self.mult(tuple(a[0:8])))
            if bcheck and sum > max_sum:
                return Fraction(1, 1)
        if ilen >= 9:
            sum += Fraction(1, a[8]) - Fraction(1, self.mult((a[0], a[8]))) - Fraction(1, self.mult((a[1], a[8]))) - Fraction(1, self.mult((a[2], a[8]))) - Fraction(1, self.mult((a[3], a[8]))) - Fraction(1, self.mult((a[4], a[8]))) - Fraction(1, self.mult((a[5], a[8]))) - Fraction(1, self.mult((a[6], a[8]))) - Fraction(1, self.mult((a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[8]))) + Fraction(1, self.mult((a[0], a[3], a[8]))) + Fraction(1, self.mult((a[0], a[4], a[8]))) + Fraction(1, self.mult((a[0], a[5], a[8]))) + Fraction(1, self.mult((a[0], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[8]))) + Fraction(1, self.mult((a[1], a[3], a[8]))) + Fraction(1, self.mult((a[1], a[4], a[8]))) + Fraction(1, self.mult((a[1], a[5], a[8]))) + Fraction(1, self.mult((a[1], a[6], a[8]))) + Fraction(1, self.mult((a[1], a[7], a[8]))) + Fraction(1, self.mult((a[2], a[3], a[8]))) + Fraction(1, self.mult((a[2], a[4], a[8]))) + Fraction(1, self.mult((a[2], a[5], a[8]))) + Fraction(1, self.mult((a[2], a[6], a[8]))) + Fraction(1, self.mult((a[2], a[7], a[8]))) + Fraction(1, self.mult((a[3], a[4], a[8]))) + Fraction(1, self.mult((a[3], a[5], a[8]))) + Fraction(1, self.mult((a[3], a[6], a[8]))) + Fraction(1, self.mult((a[3], a[7], a[8]))) + Fraction(1, self.mult((a[4], a[5], a[8]))) + Fraction(1, self.mult((a[4], a[6], a[8]))) + Fraction(1, self.mult((a[4], a[7], a[8]))) + Fraction(1, self.mult((a[5], a[6], a[8]))) + Fraction(1, self.mult((a[5], a[7], a[8]))) + Fraction(1, self.mult((a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[4], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[5], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[4], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[5], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[3], a[4], a[8]))) - Fraction(1, self.mult((a[0], a[3], a[5], a[8]))) - Fraction(1, self.mult((a[0], a[3], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[3], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[4], a[5], a[8]))) - Fraction(1, self.mult((a[0], a[4], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[4], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[4], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[5], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[6], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[3], a[4], a[8]))) - Fraction(1, self.mult((a[1], a[3], a[5], a[8]))) - Fraction(1, self.mult((a[1], a[3], a[6], a[8]))) - Fraction(1, self.mult((a[1], a[3], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[4], a[5], a[8]))) - Fraction(1, self.mult((a[1], a[4], a[6], a[8]))) - Fraction(1, self.mult((a[1], a[4], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[1], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[2], a[3], a[4], a[8]))) - Fraction(1, self.mult((a[2], a[3], a[5], a[8]))) - Fraction(1, self.mult((a[2], a[3], a[6], a[8]))) - Fraction(1, self.mult((a[2], a[3], a[7], a[8]))) - Fraction(1, self.mult((a[2], a[4], a[5], a[8]))) - Fraction(1, self.mult((a[2], a[4], a[6], a[8]))) - Fraction(1, self.mult((a[2], a[4], a[7], a[8]))) - Fraction(1, self.mult((a[2], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[2], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[2], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[3], a[4], a[5], a[8]))) - Fraction(1, self.mult((a[3], a[4], a[6], a[8]))) - Fraction(1, self.mult((a[3], a[4], a[7], a[8]))) - Fraction(1, self.mult((a[3], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[3], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[3], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[4], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[4], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[4], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[5], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[5], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[4], a[5], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[4], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[4], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[5], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[4], a[5], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[4], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[4], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[3], a[4], a[5], a[8]))) + Fraction(1, self.mult((a[0], a[3], a[4], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[3], a[4], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[3], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[3], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[3], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[4], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[4], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[4], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[5], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[6], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[4], a[5], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[4], a[6], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[4], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[3], a[4], a[5], a[8]))) + Fraction(1, self.mult((a[1], a[3], a[4], a[6], a[8]))) + Fraction(1, self.mult((a[1], a[3], a[4], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[3], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[1], a[3], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[3], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[4], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[1], a[4], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[4], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[2], a[3], a[4], a[5], a[8]))) + Fraction(1, self.mult((a[2], a[3], a[4], a[6], a[8]))) + Fraction(1, self.mult((a[2], a[3], a[4], a[7], a[8]))) + Fraction(1, self.mult((a[2], a[3], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[2], a[3], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[2], a[3], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[2], a[4], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[2], a[4], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[2], a[4], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[2], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[4], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[5], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[6], a[8])))
            sum += Fraction(-1, self.mult((a[0], a[1], a[2], a[3], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[5], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[5], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[4], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[4], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[4], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[5], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[4], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[4], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[4], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[5], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[6], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[4], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[4], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[4], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[1], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[2], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[2], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[2], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[2], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[2], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[4], a[5], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[4], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[4], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[2], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[1], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[2], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[0], a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[2], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[1], a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult((a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[2], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[1], a[3], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[0], a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, self.mult((a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, self.mult(tuple(a[0:9])))
            if bcheck and sum > max_sum:
                return Fraction(1, 1)
        return sum

    def backtrack(self, target, factors):
        global combinations
        global n
        global min_factors
        global max_factors
        if target == 1:
            if len(factors) >= min_factors and len(factors) <= max_factors and factors[0] != n:
                bappend = True
                for j in range(len(factors) - 1, 0, -1):
                    for k in range(j - 1, -1, -1):
                        if factors[j] % factors[k] == 0:
                            bappend = False
                            break
                    if not bappend:
                        break
                if bappend:
                    combinations.append(tuple(factors))
            return
        for i in sympy.divisors(target)[1:]:
            if len(factors) == 0 or (len(factors) <= 9 and i > factors[-1]):
                factors.append(i)
                self.backtrack(target // i, factors) 
                factors.pop() 
    
    
    def factorCombinations(self, i):
        #global combinations
        global n
        n = i
        #combinations = []
        #factors = []
        #self.backtrack(n, factors)
        combinations = div.Combinations(n)
        combinations.backtrack(n, [])
        return combinations
    
    
    def factorizations_outer(self, n, iminlen=3, imaxlen=10, bln_remove_gt_half=True):
        global total_factorizations_outer
        if self.verbose: print(f"factorizations_outer({n})")
        ary_tpl = factorCombinations(n)
        tfactorizations = time.time()
        at = -1
        while at < len(ary_tpl) - 1:
            at += 1
            if len(ary_tpl[at]) < self.min_factors or len(ary_tpl[at]) > self.max_factors:
                if verbose: print(f"removing ary_tpl[{at}] = {ary_tpl[at]}")
                #ary_tpl.remove(ary_tpl[at])
                ary_tpl.removeAt(at)
                # at -= 1
                continue
            #ary_tpl[at] = sorted(ary_tpl[at])
            if bln_remove_gt_half and 1/ary_tpl[at][0] + 1/ary_tpl[at][1] - 1/mult(tuple(ary_tpl[at][0:2])) + 1/ary_tpl[at][2] - 1/mult(tuple(ary_tpl[at][1:3])) - 1/mult((ary_tpl[at][0], ary_tpl[at][2])) + 1/mult(tuple(ary_tpl[at][0:3])) > 0.5:
                if verbose: print(f"removing ary_tpl[{at}] = {ary_tpl[at]}")
                # print(f"removed {ary_tpl[at]} at line 151")
                #ary_tpl.remove(ary_tpl[at])
                ary_tpl.removeAt(at)
                # at -= 1
                continue
            if False and 1/ary_tpl[at][0] + 1/ary_tpl[at][1] - 1/mult(tuple(ary_tpl[at][0:2])) > 0.5:
                if verbose: print(f"removing ary_tpl[{at}] = {ary_tpl[at]}")
                #ary_tpl.remove(ary_tpl[at])
                ary_tpl.removeAt(at)
                # at -= 1
                continue
            if False and ary_tpl[at][0] >= 9:
                if verbose: print(f"removing ary_tpl[{at}] = {ary_tpl[at]}")
                #ary_tpl.remove(ary_tpl[at])
                ary_tpl.removeAt(at)
                # at -= 1
                continue
            prev_t = ary_tpl[at][0]
            for this_t in ary_tpl[at][1:]:
                if this_t == prev_t:
                    if verbose: print(f"removing ary_tpl[{at}] = {ary_tpl[at]}")
                    #ary_tpl.remove(ary_tpl[at]) 
                    ary_tpl.removeAt(at)
                    # at -= 1
                    break
        total_factorizations_outer += (time.time() - tfactorizations)
        if self.verbose: print(f"factorizations_outer({n}) returning len(ary_tpl) = {len(ary_tpl)}")
        return ary_tpl

    
    # factors_loop(t0, i0, i1, i2, bbreak)
    def factors_loop(self):
        global max_sum
        if self.verbose: print(f"factors_loop(i1 = {self.i1}, i2 = {self.i2}), len(aryprimes) = {len(self.aryprimes)}, len(arysequence) = {len(self.arysequence)}")
        max_sum = Fraction(1, 1)
        fact2 = []
        for i in range(self.i1, self.i2):
            if self.verbose and i % 10**5 == 0:
                dt = (time.time() - self.t0)/60
                print(f"{round(dt, 2)} minutes ~ {round((i - self.i0)/dt, 1)} per min")
            if self.aryprimes[i] or (i % 2 == 0 and self.aryprimes[i//2]) or (i % 3 == 0 and self.aryprimes[i//3]) or self.arysequence[i]:
                continue
            fact1 = frozenset([tuple(ary) for ary in self.factorizations_outer(i, bln_remove_gt_half=False)])
            for f1 in fact1:
                frac1 = self.calc_density(i, f1)
                #if frac1.denominator <= 8192:
                if frac1 in self.setfractions:
                    fact2.append((frac1, i, list(f1)))
                    if self.bbreak:
                        break
            if len(fact2) >= 256:
                if self.write_to_file(sorted(fact2)):
                    fact2 = []
                else:
                    break
        if len(fact2) > 0:
            _ = self.write_to_file(sorted(fact2))
        return i


    def all_factors_loop(self):
        fact2 = []
        for i in range(self.i1, self.i2):
            if self.verbose and i % 500000 == 0:
                f.flush()
                dt = (time.time() - self.t0)/60
                print(f"{round(dt, 2)} minutes ~ {round((i - self.i0)/dt, 1)} per min")
            if self.aryprimes[i] or self.arysequence[i]:
                continue
            fact1 = frozenset([tuple(ary) for ary in self.factorizations_outer(i, bln_remove_gt_half=False)])
            for f1 in fact1:
                frac1 = self.calc_density(i, f1)
                fact2.append((frac1, i, list(f1)))
            if len(fact2) >= 256:
                fact2 = sorted(fact2)
                for f2 in fact2:
                    print(f"{f2[0]}\t\t{f2[1]:,}\t\t{f2[2]}\t\t{len(f2[2])}")
                if self.write_to_file(fact2):
                    fact2 = []
                else:
                    break
        if len(fact2) > 0:
            fact2 = sorted(fact2)
            for f2 in fact2:
                print(f"{f2[0]}\t\t{f2[1]:,}\t\t{f2[2]}\t\t{len(f2[2])}")
            _ = self.write_to_file(fact2)
        return i


    def write_to_file(self, fact2):
        global file_path
        try:
            lock = FileLock(file_path + ".lock")
            with lock:
                with open(file_path, "a") as f:
                    for f2 in fact2:
                        print(f"{f2[0]}\t\t{f2[1]:,}\t\t{f2[2]}\t\t{len(f2[2])}")
                        _ = f.write(f"{f2[0]}\t{f2[1]}\t{f2[2]}\t{len(f2[2])}\n")
            return True
        except Exception as ex:
            print(ex)
            return False


    def ary_factors_loop(self, ary):
        for i in ary:
            if self.aryprimes[i]:
                continue
            fact1 = frozenset([tuple(ary) for ary in self.factorizations_outer(i, bln_remove_gt_half=False)])
            fact2 = []
            for f1 in fact1:
                frac1 = self.calc_density(i, f1)
                if frac1.numerator == 1 or frac1.denominator <= 32:
                    fact2.append((frac1, i, list(f1)))
            for f2 in sorted(fact2):
                print(f"{f2[0]}\t\t{f2[1]:,}\t\t{f2[2]}\t\t{len(f2[2])}")


    def check_factors(self, i, print_true, print_false):
        max_sum = 0.5
        fact1 = frozenset([tuple(ary) for ary in self.factorizations_outer(i)])
        # (9, 12, 26, 235) in fact1
        blnfound = False
        for f1 in fact1:
            frac1 = self.calc_density(i, f1, max_sum)
            if frac1 in self.setfractions:
                blnfound = True
                if print_true:
                    print(f"{frac1} {i:,} {list(f1)}")
        if not blnfound and print_false:
            print(f"Not found! {i:,}")


btest = False


# results, setfractions, aryprimes, arysequence, t0, i0, i + p * imult, i + (p + 1) * imult, False, p
def factors_loop(results, setfractions, aryprimes, arysequence, t0, i0, i1, i2, bbreak, icore, bverbose):
    global btest
    # icore = icore % multiprocessing.cpu_count()
    # handle = win32api.GetCurrentProcess()
    # win32process.SetProcessAffinityMask(handle, 1 << icore)
    # psutil.Process().cpu_affinity([icore,])
    if btest:
        print(f"factors_loop(i0 = {i0}, i1 = {i1}, i2 = {i2}, icore = {icore})")
        results.put(None)
    else:
        seq = Sequence(setfractions, aryprimes, arysequence, t0, i0, i1, i2)
        seq.bbreak = bbreak
        seq.verbose = bverbose
        iseq = seq.factors_loop()
        results.put((seq.i1, seq.i2, iseq))


"""
import multiprocessing
import multiprocessing.managers
import bitarray
import sympy

class Wrapper(object):
    def __init__(self):
        self.ary = bitarray.bitarray

    def set(self, idx, val):
        self.ary[idx] = val

    def get(self, idx):
        return self.ary[idx]

multiprocessing.managers.BaseManager.register('Wrapper', Wrapper)
manager = multiprocessing.managers.BaseManager()
manager.start()
aryprimes = manager.Wrapper()

d3ef worker(obj):
	for p in sympy.sieve.primerange(2**10):
		obj.set(p, 1)

p = multiprocessing.Process(target=worker, args=(aryprimes))
p.start()
p.join()

import itertools
import time
f = open("C:\\Users\\alex.weslowski\\Documents\\Python\\Sequence\\sequence 268,435,456.txt", "r")
t0 = time.time()
i = 0
while True:
	if True:
		# 24.88 seconds (674331 lines per second)
		for line in f:
			i += 1
			ary = line.split("\t")
			if i >= 2**24:
				break
	if False:
		#  8192 ... 20.28 seconds (827284 lines per second)
		# 65536 ... 19.35 seconds (866938 lines per second)
		for line in f.readlines(65536):
			i += 1
			ary = line.split("\t")
	if False:
		#  8192 ... 21.14 seconds (793738 lines per second)
		# 65536 ... 19.68 seconds (852619 lines per second)
		for line in itertools.islice(f, 65536):
			i += 1
			ary = line.split("\t")
	if i >= 2**24:
		dt = time.time() - t0
		print(f"{round(dt, 2)} seconds ({int(round(i/dt, 0))} lines per second)")
		break
f.close()

sum([1 if x % 4 == 0 or x % 6 == 0 else 0 for x in range(1, 24 + 1)])/24
sum([1 if x % 5 == 0 or x % 6 == 0 else 0 for x in range(1, 30 + 1)])/30
sum([1 if x % 4 == 0 or x % 9 == 0 else 0 for x in range(1, 36 + 1)])/36
"""

# 
# main loop
#
# python.exe sequence_pr.py 4 [(1,2),] 2 32768
# python.exe C:\Users\alex.weslowski\Documents\Python\Sequence\sequence_pr.py 4 [(1,2),] 2 1048576
# python.exe C:\Users\alex.weslowski\Documents\Python\Sequence\sequence_pr.py 4 [(1,2),] 2 4194304
# python.exe C:\Users\alex.weslowski\Documents\Python\Sequence\sequence_pr.py 4 [(1,2),] 2 8388608
# python.exe sequence_pr.py 16 [(1,2),] 2 16777216
# python.exe sequence_pr.py 16 [(1,2),] 16777216 268435456
# python.exe sequence_pr.py 24 [(1,2),] 268550154 402653184
# python.exe sequence_pr.py 24 [(1,2),] 275722623 402653184
# python.exe sequence_pr.py 16 [(1,2),] 402653160 536870912
# 
def main():
    global file_path
    global aryprimes
    global arysequence
    global setfractions
    global i0
    global i1
    
    verbose = False
    
    if False:
        path = os.path.abspath(sys.argv[0])
        print(path)
        print(os.path.dirname(path))
        return
    
    if False:
        fact1 = [tuple(ary) for ary in factorizations_outer(14880)]
        for f1 in fact1:
            frac1 = calc_density(14880, f1)
            if frac1 in setfractions:
                print(frac1)
        
    args = sys.argv[1:]
    imult = 8192
    numcores = int(args[0])
    setfractions = frozenset([Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5),])
    setfractions = frozenset([Fraction(tpl[0], tpl[1]) for tpl in eval(args[1])])
    file_path = file_path.replace(".txt", " " + str(args[1]).replace("[", "").replace(",]", "").replace("]", "").replace(", ", ",") + ".txt")
    i0, i1 = int(args[2]) - numcores * imult, int(args[3])
    if i0 < 2:
        i0 = 2
    
    print(f"i0 = {i0}, i1 = {i1}")
    print(f"file_path = {file_path}")
    print(f"os.path.exists(file_path) = {os.path.exists(file_path)}")
    #return
    arysequence = bitarray.bitarray(i1 + 2)
    arysequence.setall(0)
    if True and os.path.exists(file_path):
        #2**29 = 536870912
        with open(file_path, "r") as f:
             this_i, prev_i = 0, 0
             while True:
                 lines = f.readlines(65536)
                 if not lines:
                     break
                 for line in lines:
                     this_i = int(line.split("\t")[1])
                     if this_i != prev_i:
                         arysequence[this_i] = 1
                         if this_i % 1048576 == 0 or this_i > i0:
                             i0 = this_i
                             print(f"{this_i:,}")
                         prev_i = this_i
        i0 -= numcores * imult
        if i0 < 2:
            i0 = 2
    
    if True:
        if i1 > len(aryprimes):
            aryprimes = bitarray.bitarray(i1 + 2)
            aryprimes.setall(0)
            try:
                for p in primesieve.primes(i1 + 2):
                    aryprimes[p] = 1
            except NameError as ne:
                for p in sympy.sieve.primerange(i1 + 2):
                    aryprimes[p] = 1
                pass

    icurrent, t0 = i0, time.time()
    seq = Sequence(setfractions, aryprimes, arysequence, t0, i0, i1, i1)    
    if Fraction(1, 2) in setfractions:
        if i0 <= 2:
            seq.write_to_file([(Fraction(1, 2), 2, [2,])])
        if i0 <= 12:
            seq.write_to_file([(Fraction(1, 2), 12, [3, 4])])
    if Fraction(1, 3) in setfractions:
        if i0 <= 3:
            seq.write_to_file([(Fraction(1, 3), 3, [3,])])
    
    print(f"starting process with numcores={numcores}, istart={i0}, ifinish={i1}")
    print(f"len(aryprimes) = {len(aryprimes):,}, len(arysequence) = {len(arysequence):,}")
    print(f"sizeof(aryprimes) = {round(sys.getsizeof(aryprimes)/(1024 * 1024), 1)} MB, sizeof(arysequence) = {round(sys.getsizeof(arysequence)/(1024 * 1024), 1)} MB")
    #return
    results = Queue()
    while icurrent < i1:
        pr = [None,] * numcores
        icountp = 0
        for p in range(0, numcores):
            #print(f"Process(args=({i0}, {icurrent + p * imult}, {icurrent + (p + 1) * imult}))")
            pr[p] = Process(target=factors_loop, args=(results, setfractions, aryprimes, arysequence, t0, i0, icurrent + p * imult, icurrent + (p + 1) * imult, False, p, verbose))
            pr[p].start()
            icountp += 1
            if icurrent + (p + 1) * imult >= i1:
                break
        for p in range(0, numcores):
            if pr[p]:
                pr[p].join()
        p = 0
        while p < icountp:
            try:
                tpl = results.get(timeout=1)
                if verbose: print(f"{tpl} ({p}/{icountp})")
                p += 1
            except Empty:
                pass
        icurrent += numcores * imult
        if verbose: print(f"icurrent = {icurrent}, i1 = {i1}")
    
    dt = (time.time() - t0)/60
    sdt = f"{round(dt, 2)} minutes" if dt < 60 else f"{round(dt/60, 2)} hours"
    print(f"{sdt} ~ {round((i1 - i0)/dt):,} per min")


if __name__ == '__main__':
    main()

