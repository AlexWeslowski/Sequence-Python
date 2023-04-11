import pyjion, sys, multiprocessing, math, itertools, functools, operator, primefac, primesieve, fractions, time
from fractions import Fraction
from multiprocessing import Process
# 2**28 ~ 10**8.43
# 2**33 ~ 10**9.93
setprimes = frozenset(primesieve.primes(2**28))
setfractions = frozenset([Fraction(1, 2),])

@functools.cache
def gcd(tpl):
    return math.gcd(tpl[0], tpl[1])


@functools.cache
def lcm(tpl):
    return math.lcm(tpl[0], tpl[1])


def lcm2(tpl):
    t1 = tpl[-1]
    for t2 in tpl[-2::-1]:
        t1 = math.lcm(t2, t1)
    return t1


@functools.cache
def mult(tpl):
    global setprimes
    ary = list(tpl)
    if True:
        ilen = len(ary)
        # ary[1] = ary[0]*ary[1] if ary[0] in setprimes or ary[1] in setprimes else ary[0]*ary[1]//gcd((ary[0], ary[1]))
        ary[1] = ary[0]*ary[1] if ary[0] in setprimes or ary[1] in setprimes else lcm((ary[0], ary[1]))
        if ilen <= 2:
            return ary[1]
        else:
            for a in range(2, 10 + 1):
                # ary[a] = ary[a - 1]*ary[a] if ary[a] in setprimes else ary[a - 1]*ary[a]//gcd((ary[a - 1], ary[a]))
                ary[a] = ary[a - 1]*ary[a] if ary[a] in setprimes else lcm((ary[a - 1], ary[a]))
                if ilen <= a + 1:
                    return ary[a]


def calc_density(i, a):
    ilen = len(a)
    sum = Fraction(1, a[0])
    if sum > 0.5:
        return Fraction(1, 1)
    sum += Fraction(1, a[1]) - Fraction(1, mult(tuple(a[0:2])))
    if sum > 0.5:
        return 1.0
    if ilen >= 3:
        sum += Fraction(1, a[2]) - Fraction(1, mult((a[0], a[2]))) - Fraction(1, mult((a[1], a[2]))) + Fraction(1, mult(tuple(a[0:3])))
        if sum > 0.5:
            return Fraction(1, 1)
        
    if ilen >= 4:
        sum += Fraction(1, a[3]) - Fraction(1, mult((a[0], a[3]))) - Fraction(1, mult((a[1], a[3]))) - Fraction(1, mult((a[2], a[3]))) + Fraction(1, mult((a[0], a[1], a[3]))) + Fraction(1, mult((a[0], a[2], a[3]))) + Fraction(1, mult((a[1], a[2], a[3]))) - Fraction(1, mult(tuple(a[0:4])))
        if sum > 0.5:
            return Fraction(1, 1)
        
    if ilen >= 5:
        sum += Fraction(1, a[4]) - Fraction(1, mult((a[0], a[4]))) - Fraction(1, mult((a[1], a[4]))) - Fraction(1, mult((a[2], a[4]))) - Fraction(1, mult((a[3], a[4]))) + Fraction(1, mult((a[0], a[1], a[4]))) + Fraction(1, mult((a[0], a[2], a[4]))) + Fraction(1, mult((a[0], a[3], a[4]))) + Fraction(1, mult((a[1], a[2], a[4]))) + Fraction(1, mult((a[1], a[3], a[4]))) + Fraction(1, mult((a[2], a[3], a[4]))) - Fraction(1, mult((a[0], a[1], a[2], a[4]))) - Fraction(1, mult((a[0], a[1], a[3], a[4]))) - Fraction(1, mult((a[0], a[2], a[3], a[4]))) - Fraction(1, mult((a[1], a[2], a[3], a[4]))) + Fraction(1, mult(tuple(a[0:5])))
        if sum > 0.5:
            return Fraction(1, 1)
        
    if ilen >= 6:
        sum += Fraction(1, a[5]) - Fraction(1, mult((a[0], a[5]))) - Fraction(1, mult((a[1], a[5]))) - Fraction(1, mult((a[2], a[5]))) - Fraction(1, mult((a[3], a[5]))) - Fraction(1, mult((a[4], a[5]))) + Fraction(1, mult((a[0], a[1], a[5]))) + Fraction(1, mult((a[0], a[2], a[5]))) + Fraction(1, mult((a[0], a[3], a[5]))) + Fraction(1, mult((a[0], a[4], a[5]))) + Fraction(1, mult((a[1], a[2], a[5]))) + Fraction(1, mult((a[1], a[3], a[5]))) + Fraction(1, mult((a[1], a[4], a[5]))) + Fraction(1, mult((a[2], a[3], a[5]))) + Fraction(1, mult((a[2], a[4], a[5]))) + Fraction(1, mult((a[3], a[4], a[5]))) - Fraction(1, mult((a[0], a[1], a[2], a[5]))) - Fraction(1, mult((a[0], a[1], a[3], a[5]))) - Fraction(1, mult((a[0], a[1], a[4], a[5]))) - Fraction(1, mult((a[0], a[2], a[3], a[5]))) - Fraction(1, mult((a[0], a[2], a[4], a[5]))) - Fraction(1, mult((a[0], a[3], a[4], a[5]))) - Fraction(1, mult((a[1], a[2], a[3], a[5]))) - Fraction(1, mult((a[1], a[2], a[4], a[5]))) - Fraction(1, mult((a[1], a[3], a[4], a[5]))) - Fraction(1, mult((a[2], a[3], a[4], a[5]))) + Fraction(1, mult((a[0], a[1], a[2], a[3], a[5]))) + Fraction(1, mult((a[0], a[1], a[2], a[4], a[5]))) + Fraction(1, mult((a[0], a[1], a[3], a[4], a[5]))) + Fraction(1, mult((a[0], a[2], a[3], a[4], a[5]))) + Fraction(1, mult((a[1], a[2], a[3], a[4], a[5]))) - Fraction(1, mult(tuple(a[0:6])))
        if sum > 0.5:
            return Fraction(1, 1)
        
    if ilen >= 7:
        sum += Fraction(1, a[6]) - Fraction(1, mult((a[0], a[6]))) - Fraction(1, mult((a[1], a[6]))) - Fraction(1, mult((a[2], a[6]))) - Fraction(1, mult((a[3], a[6]))) - Fraction(1, mult((a[4], a[6]))) - Fraction(1, mult((a[5], a[6]))) + Fraction(1, mult((a[0], a[1], a[6]))) + Fraction(1, mult((a[0], a[2], a[6]))) + Fraction(1, mult((a[0], a[3], a[6]))) + Fraction(1, mult((a[0], a[4], a[6]))) + Fraction(1, mult((a[0], a[5], a[6]))) + Fraction(1, mult((a[1], a[2], a[6]))) + Fraction(1, mult((a[1], a[3], a[6]))) + Fraction(1, mult((a[1], a[4], a[6]))) + Fraction(1, mult((a[1], a[5], a[6]))) + Fraction(1, mult((a[2], a[3], a[6]))) + Fraction(1, mult((a[2], a[4], a[6]))) + Fraction(1, mult((a[2], a[5], a[6]))) + Fraction(1, mult((a[3], a[4], a[6]))) + Fraction(1, mult((a[3], a[5], a[6]))) + Fraction(1, mult((a[4], a[5], a[6]))) - Fraction(1, mult((a[0], a[1], a[2], a[6]))) - Fraction(1, mult((a[0], a[1], a[3], a[6]))) - Fraction(1, mult((a[0], a[1], a[4], a[6]))) - Fraction(1, mult((a[0], a[1], a[5], a[6]))) - Fraction(1, mult((a[0], a[2], a[3], a[6]))) - Fraction(1, mult((a[0], a[2], a[4], a[6]))) - Fraction(1, mult((a[0], a[2], a[5], a[6]))) - Fraction(1, mult((a[0], a[3], a[4], a[6]))) - Fraction(1, mult((a[0], a[3], a[5], a[6]))) - Fraction(1, mult((a[0], a[4], a[5], a[6]))) - Fraction(1, mult((a[1], a[2], a[3], a[6]))) - Fraction(1, mult((a[1], a[2], a[4], a[6]))) - Fraction(1, mult((a[1], a[2], a[5], a[6]))) - Fraction(1, mult((a[1], a[3], a[4], a[6]))) - Fraction(1, mult((a[1], a[3], a[5], a[6]))) - Fraction(1, mult((a[1], a[4], a[5], a[6]))) - Fraction(1, mult((a[2], a[3], a[4], a[6]))) - Fraction(1, mult((a[2], a[3], a[5], a[6]))) - Fraction(1, mult((a[2], a[4], a[5], a[6]))) - Fraction(1, mult((a[3], a[4], a[5], a[6]))) + Fraction(1, mult((a[0], a[1], a[2], a[3], a[6]))) + Fraction(1, mult((a[0], a[1], a[2], a[4], a[6]))) + Fraction(1, mult((a[0], a[1], a[2], a[5], a[6]))) + Fraction(1, mult((a[0], a[1], a[3], a[4], a[6]))) + Fraction(1, mult((a[0], a[1], a[3], a[5], a[6]))) + Fraction(1, mult((a[0], a[1], a[4], a[5], a[6]))) + Fraction(1, mult((a[0], a[2], a[3], a[4], a[6]))) + Fraction(1, mult((a[0], a[2], a[3], a[5], a[6]))) + Fraction(1, mult((a[0], a[2], a[4], a[5], a[6]))) + Fraction(1, mult((a[0], a[3], a[4], a[5], a[6]))) + Fraction(1, mult((a[1], a[2], a[3], a[4], a[6]))) + Fraction(1, mult((a[1], a[2], a[3], a[5], a[6]))) + Fraction(1, mult((a[1], a[2], a[4], a[5], a[6]))) + Fraction(1, mult((a[1], a[3], a[4], a[5], a[6]))) + Fraction(1, mult((a[2], a[3], a[4], a[5], a[6]))) - Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[6]))) - Fraction(1, mult((a[0], a[1], a[2], a[3], a[5], a[6]))) - Fraction(1, mult((a[0], a[1], a[2], a[4], a[5], a[6]))) - Fraction(1, mult((a[0], a[1], a[3], a[4], a[5], a[6]))) - Fraction(1, mult((a[0], a[2], a[3], a[4], a[5], a[6]))) - Fraction(1, mult((a[1], a[2], a[3], a[4], a[5], a[6]))) + Fraction(1, mult(tuple(a[0:7])))
        if sum > 0.5:
            return Fraction(1, 1)
        
    if ilen >= 8:
        sum += Fraction(1, a[7]) - Fraction(1, mult((a[0], a[7]))) - Fraction(1, mult((a[1], a[7]))) - Fraction(1, mult((a[2], a[7]))) - Fraction(1, mult((a[3], a[7]))) - Fraction(1, mult((a[4], a[7]))) - Fraction(1, mult((a[5], a[7]))) - Fraction(1, mult((a[6], a[7]))) + Fraction(1, mult((a[0], a[1], a[7]))) + Fraction(1, mult((a[0], a[2], a[7]))) + Fraction(1, mult((a[0], a[3], a[7]))) + Fraction(1, mult((a[0], a[4], a[7]))) + Fraction(1, mult((a[0], a[5], a[7]))) + Fraction(1, mult((a[0], a[6], a[7]))) + Fraction(1, mult((a[1], a[2], a[7]))) + Fraction(1, mult((a[1], a[3], a[7]))) + Fraction(1, mult((a[1], a[4], a[7]))) + Fraction(1, mult((a[1], a[5], a[7]))) + Fraction(1, mult((a[1], a[6], a[7]))) + Fraction(1, mult((a[2], a[3], a[7]))) + Fraction(1, mult((a[2], a[4], a[7]))) + Fraction(1, mult((a[2], a[5], a[7]))) + Fraction(1, mult((a[2], a[6], a[7]))) + Fraction(1, mult((a[3], a[4], a[7]))) + Fraction(1, mult((a[3], a[5], a[7]))) + Fraction(1, mult((a[3], a[6], a[7]))) + Fraction(1, mult((a[4], a[5], a[7]))) + Fraction(1, mult((a[4], a[6], a[7]))) + Fraction(1, mult((a[5], a[6], a[7]))) - Fraction(1, mult((a[0], a[1], a[2], a[7]))) - Fraction(1, mult((a[0], a[1], a[3], a[7]))) - Fraction(1, mult((a[0], a[1], a[4], a[7]))) - Fraction(1, mult((a[0], a[1], a[5], a[7]))) - Fraction(1, mult((a[0], a[1], a[6], a[7]))) - Fraction(1, mult((a[0], a[2], a[3], a[7]))) - Fraction(1, mult((a[0], a[2], a[4], a[7]))) - Fraction(1, mult((a[0], a[2], a[5], a[7]))) - Fraction(1, mult((a[0], a[2], a[6], a[7]))) - Fraction(1, mult((a[0], a[3], a[4], a[7]))) - Fraction(1, mult((a[0], a[3], a[5], a[7]))) - Fraction(1, mult((a[0], a[3], a[6], a[7]))) - Fraction(1, mult((a[0], a[4], a[5], a[7]))) - Fraction(1, mult((a[0], a[4], a[6], a[7]))) - Fraction(1, mult((a[0], a[5], a[6], a[7]))) - Fraction(1, mult((a[1], a[2], a[3], a[7]))) - Fraction(1, mult((a[1], a[2], a[4], a[7]))) - Fraction(1, mult((a[1], a[2], a[5], a[7]))) - Fraction(1, mult((a[1], a[2], a[6], a[7]))) - Fraction(1, mult((a[1], a[3], a[4], a[7]))) - Fraction(1, mult((a[1], a[3], a[5], a[7]))) - Fraction(1, mult((a[1], a[3], a[6], a[7]))) - Fraction(1, mult((a[1], a[4], a[5], a[7]))) - Fraction(1, mult((a[1], a[4], a[6], a[7]))) - Fraction(1, mult((a[1], a[5], a[6], a[7]))) - Fraction(1, mult((a[2], a[3], a[4], a[7]))) - Fraction(1, mult((a[2], a[3], a[5], a[7]))) - Fraction(1, mult((a[2], a[3], a[6], a[7]))) - Fraction(1, mult((a[2], a[4], a[5], a[7]))) - Fraction(1, mult((a[2], a[4], a[6], a[7]))) - Fraction(1, mult((a[2], a[5], a[6], a[7]))) - Fraction(1, mult((a[3], a[4], a[5], a[7]))) - Fraction(1, mult((a[3], a[4], a[6], a[7]))) - Fraction(1, mult((a[3], a[5], a[6], a[7]))) - Fraction(1, mult((a[4], a[5], a[6], a[7]))) + Fraction(1, mult((a[0], a[1], a[2], a[3], a[7]))) + Fraction(1, mult((a[0], a[1], a[2], a[4], a[7]))) + Fraction(1, mult((a[0], a[1], a[2], a[5], a[7]))) + Fraction(1, mult((a[0], a[1], a[2], a[6], a[7]))) + Fraction(1, mult((a[0], a[1], a[3], a[4], a[7]))) + Fraction(1, mult((a[0], a[1], a[3], a[5], a[7]))) + Fraction(1, mult((a[0], a[1], a[3], a[6], a[7]))) + Fraction(1, mult((a[0], a[1], a[4], a[5], a[7])))
        sum += Fraction(1, mult((a[0], a[1], a[4], a[6], a[7]))) + Fraction(1, mult((a[0], a[1], a[5], a[6], a[7]))) + Fraction(1, mult((a[0], a[2], a[3], a[4], a[7]))) + Fraction(1, mult((a[0], a[2], a[3], a[5], a[7]))) + Fraction(1, mult((a[0], a[2], a[3], a[6], a[7]))) + Fraction(1, mult((a[0], a[2], a[4], a[5], a[7]))) + Fraction(1, mult((a[0], a[2], a[4], a[6], a[7]))) + Fraction(1, mult((a[0], a[2], a[5], a[6], a[7]))) + Fraction(1, mult((a[0], a[3], a[4], a[5], a[7]))) + Fraction(1, mult((a[0], a[3], a[4], a[6], a[7]))) + Fraction(1, mult((a[0], a[3], a[5], a[6], a[7]))) + Fraction(1, mult((a[0], a[4], a[5], a[6], a[7]))) + Fraction(1, mult((a[1], a[2], a[3], a[4], a[7]))) + Fraction(1, mult((a[1], a[2], a[3], a[5], a[7]))) + Fraction(1, mult((a[1], a[2], a[3], a[6], a[7]))) + Fraction(1, mult((a[1], a[2], a[4], a[5], a[7]))) + Fraction(1, mult((a[1], a[2], a[4], a[6], a[7]))) + Fraction(1, mult((a[1], a[2], a[5], a[6], a[7]))) + Fraction(1, mult((a[1], a[3], a[4], a[5], a[7]))) + Fraction(1, mult((a[1], a[3], a[4], a[6], a[7]))) + Fraction(1, mult((a[1], a[3], a[5], a[6], a[7]))) + Fraction(1, mult((a[1], a[4], a[5], a[6], a[7]))) + Fraction(1, mult((a[2], a[3], a[4], a[5], a[7]))) + Fraction(1, mult((a[2], a[3], a[4], a[6], a[7]))) + Fraction(1, mult((a[2], a[3], a[5], a[6], a[7]))) + Fraction(1, mult((a[2], a[4], a[5], a[6], a[7]))) + Fraction(1, mult((a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[7]))) - Fraction(1, mult((a[0], a[1], a[2], a[3], a[5], a[7]))) - Fraction(1, mult((a[0], a[1], a[2], a[3], a[6], a[7]))) - Fraction(1, mult((a[0], a[1], a[2], a[4], a[5], a[7]))) - Fraction(1, mult((a[0], a[1], a[2], a[4], a[6], a[7]))) - Fraction(1, mult((a[0], a[1], a[2], a[5], a[6], a[7]))) - Fraction(1, mult((a[0], a[1], a[3], a[4], a[5], a[7]))) - Fraction(1, mult((a[0], a[1], a[3], a[4], a[6], a[7]))) - Fraction(1, mult((a[0], a[1], a[3], a[5], a[6], a[7]))) - Fraction(1, mult((a[0], a[1], a[4], a[5], a[6], a[7]))) - Fraction(1, mult((a[0], a[2], a[3], a[4], a[5], a[7]))) - Fraction(1, mult((a[0], a[2], a[3], a[4], a[6], a[7]))) - Fraction(1, mult((a[0], a[2], a[3], a[5], a[6], a[7]))) - Fraction(1, mult((a[0], a[2], a[4], a[5], a[6], a[7]))) - Fraction(1, mult((a[0], a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, mult((a[1], a[2], a[3], a[4], a[5], a[7]))) - Fraction(1, mult((a[1], a[2], a[3], a[4], a[6], a[7]))) - Fraction(1, mult((a[1], a[2], a[3], a[5], a[6], a[7]))) - Fraction(1, mult((a[1], a[2], a[4], a[5], a[6], a[7]))) - Fraction(1, mult((a[1], a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, mult((a[2], a[3], a[4], a[5], a[6], a[7]))) + Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[5], a[7]))) + Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[6], a[7]))) + Fraction(1, mult((a[0], a[1], a[2], a[3], a[5], a[6], a[7]))) + Fraction(1, mult((a[0], a[1], a[2], a[4], a[5], a[6], a[7]))) + Fraction(1, mult((a[0], a[1], a[3], a[4], a[5], a[6], a[7]))) + Fraction(1, mult((a[0], a[2], a[3], a[4], a[5], a[6], a[7]))) + Fraction(1, mult((a[1], a[2], a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, mult(tuple(a[0:8])))
        if sum > 0.5:
            return Fraction(1, 1)
        
    if ilen >= 9:
        sum += Fraction(1, a[8]) - Fraction(1, mult((a[0], a[8]))) - Fraction(1, mult((a[1], a[8]))) - Fraction(1, mult((a[2], a[8]))) - Fraction(1, mult((a[3], a[8]))) - Fraction(1, mult((a[4], a[8]))) - Fraction(1, mult((a[5], a[8]))) - Fraction(1, mult((a[6], a[8]))) - Fraction(1, mult((a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[8]))) + Fraction(1, mult((a[0], a[2], a[8]))) + Fraction(1, mult((a[0], a[3], a[8]))) + Fraction(1, mult((a[0], a[4], a[8]))) + Fraction(1, mult((a[0], a[5], a[8]))) + Fraction(1, mult((a[0], a[6], a[8]))) + Fraction(1, mult((a[0], a[7], a[8]))) + Fraction(1, mult((a[1], a[2], a[8]))) + Fraction(1, mult((a[1], a[3], a[8]))) + Fraction(1, mult((a[1], a[4], a[8]))) + Fraction(1, mult((a[1], a[5], a[8]))) + Fraction(1, mult((a[1], a[6], a[8]))) + Fraction(1, mult((a[1], a[7], a[8]))) + Fraction(1, mult((a[2], a[3], a[8]))) + Fraction(1, mult((a[2], a[4], a[8]))) + Fraction(1, mult((a[2], a[5], a[8]))) + Fraction(1, mult((a[2], a[6], a[8]))) + Fraction(1, mult((a[2], a[7], a[8]))) + Fraction(1, mult((a[3], a[4], a[8]))) + Fraction(1, mult((a[3], a[5], a[8]))) + Fraction(1, mult((a[3], a[6], a[8]))) + Fraction(1, mult((a[3], a[7], a[8]))) + Fraction(1, mult((a[4], a[5], a[8]))) + Fraction(1, mult((a[4], a[6], a[8]))) + Fraction(1, mult((a[4], a[7], a[8]))) + Fraction(1, mult((a[5], a[6], a[8]))) + Fraction(1, mult((a[5], a[7], a[8]))) + Fraction(1, mult((a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[8]))) - Fraction(1, mult((a[0], a[1], a[3], a[8]))) - Fraction(1, mult((a[0], a[1], a[4], a[8]))) - Fraction(1, mult((a[0], a[1], a[5], a[8]))) - Fraction(1, mult((a[0], a[1], a[6], a[8]))) - Fraction(1, mult((a[0], a[1], a[7], a[8]))) - Fraction(1, mult((a[0], a[2], a[3], a[8]))) - Fraction(1, mult((a[0], a[2], a[4], a[8]))) - Fraction(1, mult((a[0], a[2], a[5], a[8]))) - Fraction(1, mult((a[0], a[2], a[6], a[8]))) - Fraction(1, mult((a[0], a[2], a[7], a[8]))) - Fraction(1, mult((a[0], a[3], a[4], a[8]))) - Fraction(1, mult((a[0], a[3], a[5], a[8]))) - Fraction(1, mult((a[0], a[3], a[6], a[8]))) - Fraction(1, mult((a[0], a[3], a[7], a[8]))) - Fraction(1, mult((a[0], a[4], a[5], a[8]))) - Fraction(1, mult((a[0], a[4], a[6], a[8]))) - Fraction(1, mult((a[0], a[4], a[7], a[8]))) - Fraction(1, mult((a[0], a[5], a[6], a[8]))) - Fraction(1, mult((a[0], a[5], a[7], a[8]))) - Fraction(1, mult((a[0], a[6], a[7], a[8]))) - Fraction(1, mult((a[1], a[2], a[3], a[8]))) - Fraction(1, mult((a[1], a[2], a[4], a[8]))) - Fraction(1, mult((a[1], a[2], a[5], a[8]))) - Fraction(1, mult((a[1], a[2], a[6], a[8]))) - Fraction(1, mult((a[1], a[2], a[7], a[8]))) - Fraction(1, mult((a[1], a[3], a[4], a[8]))) - Fraction(1, mult((a[1], a[3], a[5], a[8]))) - Fraction(1, mult((a[1], a[3], a[6], a[8]))) - Fraction(1, mult((a[1], a[3], a[7], a[8]))) - Fraction(1, mult((a[1], a[4], a[5], a[8]))) - Fraction(1, mult((a[1], a[4], a[6], a[8]))) - Fraction(1, mult((a[1], a[4], a[7], a[8]))) - Fraction(1, mult((a[1], a[5], a[6], a[8]))) - Fraction(1, mult((a[1], a[5], a[7], a[8]))) - Fraction(1, mult((a[1], a[6], a[7], a[8]))) - Fraction(1, mult((a[2], a[3], a[4], a[8]))) - Fraction(1, mult((a[2], a[3], a[5], a[8]))) - Fraction(1, mult((a[2], a[3], a[6], a[8]))) - Fraction(1, mult((a[2], a[3], a[7], a[8]))) - Fraction(1, mult((a[2], a[4], a[5], a[8]))) - Fraction(1, mult((a[2], a[4], a[6], a[8]))) - Fraction(1, mult((a[2], a[4], a[7], a[8]))) - Fraction(1, mult((a[2], a[5], a[6], a[8]))) - Fraction(1, mult((a[2], a[5], a[7], a[8]))) - Fraction(1, mult((a[2], a[6], a[7], a[8]))) - Fraction(1, mult((a[3], a[4], a[5], a[8]))) - Fraction(1, mult((a[3], a[4], a[6], a[8]))) - Fraction(1, mult((a[3], a[4], a[7], a[8]))) - Fraction(1, mult((a[3], a[5], a[6], a[8]))) - Fraction(1, mult((a[3], a[5], a[7], a[8]))) - Fraction(1, mult((a[3], a[6], a[7], a[8]))) - Fraction(1, mult((a[4], a[5], a[6], a[8]))) - Fraction(1, mult((a[4], a[5], a[7], a[8]))) - Fraction(1, mult((a[4], a[6], a[7], a[8]))) - Fraction(1, mult((a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[3], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[4], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[5], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[6], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[3], a[4], a[8]))) + Fraction(1, mult((a[0], a[1], a[3], a[5], a[8]))) + Fraction(1, mult((a[0], a[1], a[3], a[6], a[8]))) + Fraction(1, mult((a[0], a[1], a[3], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[4], a[5], a[8]))) + Fraction(1, mult((a[0], a[1], a[4], a[6], a[8]))) + Fraction(1, mult((a[0], a[1], a[4], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[5], a[6], a[8]))) + Fraction(1, mult((a[0], a[1], a[5], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[2], a[3], a[4], a[8]))) + Fraction(1, mult((a[0], a[2], a[3], a[5], a[8]))) + Fraction(1, mult((a[0], a[2], a[3], a[6], a[8]))) + Fraction(1, mult((a[0], a[2], a[3], a[7], a[8]))) + Fraction(1, mult((a[0], a[2], a[4], a[5], a[8]))) + Fraction(1, mult((a[0], a[2], a[4], a[6], a[8]))) + Fraction(1, mult((a[0], a[2], a[4], a[7], a[8]))) + Fraction(1, mult((a[0], a[2], a[5], a[6], a[8]))) + Fraction(1, mult((a[0], a[2], a[5], a[7], a[8]))) + Fraction(1, mult((a[0], a[2], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[3], a[4], a[5], a[8]))) + Fraction(1, mult((a[0], a[3], a[4], a[6], a[8]))) + Fraction(1, mult((a[0], a[3], a[4], a[7], a[8]))) + Fraction(1, mult((a[0], a[3], a[5], a[6], a[8]))) + Fraction(1, mult((a[0], a[3], a[5], a[7], a[8]))) + Fraction(1, mult((a[0], a[3], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[4], a[5], a[6], a[8]))) + Fraction(1, mult((a[0], a[4], a[5], a[7], a[8]))) + Fraction(1, mult((a[0], a[4], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[1], a[2], a[3], a[4], a[8]))) + Fraction(1, mult((a[1], a[2], a[3], a[5], a[8]))) + Fraction(1, mult((a[1], a[2], a[3], a[6], a[8]))) + Fraction(1, mult((a[1], a[2], a[3], a[7], a[8]))) + Fraction(1, mult((a[1], a[2], a[4], a[5], a[8]))) + Fraction(1, mult((a[1], a[2], a[4], a[6], a[8]))) + Fraction(1, mult((a[1], a[2], a[4], a[7], a[8]))) + Fraction(1, mult((a[1], a[2], a[5], a[6], a[8]))) + Fraction(1, mult((a[1], a[2], a[5], a[7], a[8]))) + Fraction(1, mult((a[1], a[2], a[6], a[7], a[8]))) + Fraction(1, mult((a[1], a[3], a[4], a[5], a[8]))) + Fraction(1, mult((a[1], a[3], a[4], a[6], a[8]))) + Fraction(1, mult((a[1], a[3], a[4], a[7], a[8]))) + Fraction(1, mult((a[1], a[3], a[5], a[6], a[8]))) + Fraction(1, mult((a[1], a[3], a[5], a[7], a[8]))) + Fraction(1, mult((a[1], a[3], a[6], a[7], a[8]))) + Fraction(1, mult((a[1], a[4], a[5], a[6], a[8]))) + Fraction(1, mult((a[1], a[4], a[5], a[7], a[8]))) + Fraction(1, mult((a[1], a[4], a[6], a[7], a[8]))) + Fraction(1, mult((a[1], a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[2], a[3], a[4], a[5], a[8]))) + Fraction(1, mult((a[2], a[3], a[4], a[6], a[8]))) + Fraction(1, mult((a[2], a[3], a[4], a[7], a[8]))) + Fraction(1, mult((a[2], a[3], a[5], a[6], a[8]))) + Fraction(1, mult((a[2], a[3], a[5], a[7], a[8]))) + Fraction(1, mult((a[2], a[3], a[6], a[7], a[8]))) + Fraction(1, mult((a[2], a[4], a[5], a[6], a[8]))) + Fraction(1, mult((a[2], a[4], a[5], a[7], a[8]))) + Fraction(1, mult((a[2], a[4], a[6], a[7], a[8]))) + Fraction(1, mult((a[2], a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, mult((a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, mult((a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, mult((a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[3], a[5], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[3], a[6], a[8])))
        sum += Fraction(-1, mult((a[0], a[1], a[2], a[3], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[4], a[5], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[4], a[6], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[4], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[5], a[6], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[5], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[3], a[4], a[5], a[8]))) - Fraction(1, mult((a[0], a[1], a[3], a[4], a[6], a[8]))) - Fraction(1, mult((a[0], a[1], a[3], a[4], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[3], a[5], a[6], a[8]))) - Fraction(1, mult((a[0], a[1], a[3], a[5], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[3], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[4], a[5], a[6], a[8]))) - Fraction(1, mult((a[0], a[1], a[4], a[5], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[4], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[2], a[3], a[4], a[5], a[8]))) - Fraction(1, mult((a[0], a[2], a[3], a[4], a[6], a[8]))) - Fraction(1, mult((a[0], a[2], a[3], a[4], a[7], a[8]))) - Fraction(1, mult((a[0], a[2], a[3], a[5], a[6], a[8]))) - Fraction(1, mult((a[0], a[2], a[3], a[5], a[7], a[8]))) - Fraction(1, mult((a[0], a[2], a[3], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[2], a[4], a[5], a[6], a[8]))) - Fraction(1, mult((a[0], a[2], a[4], a[5], a[7], a[8]))) - Fraction(1, mult((a[0], a[2], a[4], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[2], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, mult((a[0], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, mult((a[0], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[1], a[2], a[3], a[4], a[5], a[8]))) - Fraction(1, mult((a[1], a[2], a[3], a[4], a[6], a[8]))) - Fraction(1, mult((a[1], a[2], a[3], a[4], a[7], a[8]))) - Fraction(1, mult((a[1], a[2], a[3], a[5], a[6], a[8]))) - Fraction(1, mult((a[1], a[2], a[3], a[5], a[7], a[8]))) - Fraction(1, mult((a[1], a[2], a[3], a[6], a[7], a[8]))) - Fraction(1, mult((a[1], a[2], a[4], a[5], a[6], a[8]))) - Fraction(1, mult((a[1], a[2], a[4], a[5], a[7], a[8]))) - Fraction(1, mult((a[1], a[2], a[4], a[6], a[7], a[8]))) - Fraction(1, mult((a[1], a[2], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[1], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, mult((a[1], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, mult((a[1], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, mult((a[1], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[1], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[2], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, mult((a[2], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, mult((a[2], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, mult((a[2], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[2], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[5], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[6], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[3], a[5], a[6], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[3], a[5], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[3], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[4], a[5], a[6], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[4], a[5], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[4], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[2], a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, mult((a[0], a[1], a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[1], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[2], a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, mult((a[0], a[2], a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, mult((a[0], a[2], a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[2], a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[2], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[0], a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[1], a[2], a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, mult((a[1], a[2], a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, mult((a[1], a[2], a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, mult((a[1], a[2], a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[1], a[2], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[1], a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult((a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[2], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[1], a[3], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[0], a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult((a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult(tuple(a[0:9])))
        if sum > 0.5:
            return Fraction(1, 1)
    
    return sum


def backtrack(start, target, factors, combinations, n):
    if target == 1:
        # Add a copy of the factors list to combinations, except if the list contains only one factor equal to n
        if (len(factors) >= 4 and len(factors) <= 9) and (factors[0] != n and factors[0] != 2):
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
    
    for i in range(start, target + 1):
        if target % i == 0:
            if len(factors) == 0 or factors[-1] != i:
                    factors.append(i) # Add i to factors
                    backtrack(i, target // i, factors, combinations, n) # Recursively find factors of target // i
                    factors.pop() # Remove i from factors


def factorCombinations(n):
    combinations = []
    factors = []
    backtrack(2, n, factors, combinations, n)
    return combinations


def factorizations_outer(n, iminlen=3, imaxlen=10):
    ary_tpl = factorCombinations(n)
    at = -1
    while at < len(ary_tpl) - 1:
        at += 1
        if len(ary_tpl[at]) < iminlen or len(ary_tpl[at]) > imaxlen:
            ary_tpl.remove(ary_tpl[at])
            # at -= 1
            continue
        ary_tpl[at] = sorted(ary_tpl[at])
        if True and 1/ary_tpl[at][0] + 1/ary_tpl[at][1] - 1/mult(tuple(ary_tpl[at][0:2])) + 1/ary_tpl[at][2] - 1/mult(tuple(ary_tpl[at][1:3])) - 1/mult((ary_tpl[at][0], ary_tpl[at][2])) + 1/mult(tuple(ary_tpl[at][0:3])) > 0.5:
             ary_tpl.remove(ary_tpl[at])
             # at -= 1
             continue
        if False and 1/ary_tpl[at][0] + 1/ary_tpl[at][1] - 1/mult(tuple(ary_tpl[at][0:2])) > 0.5:
             ary_tpl.remove(ary_tpl[at])
             # at -= 1
             continue
        if ary_tpl[at][0] >= 9:
            ary_tpl.remove(ary_tpl[at])
            # at -= 1
            continue
        prev_t = ary_tpl[at][0]
        for this_t in ary_tpl[at][1:]:
            if this_t == prev_t:
                ary_tpl.remove(ary_tpl[at]) 
                # at -= 1
                break
    return ary_tpl


def factors_loop(t0, i0, i1, i2, bbreak):
    for i in range(i1, i2):
        if i % 50000 == 0:
            dt = (time.time() - t0)/60
            print(f"{round(dt, 2)} minutes ~ {round((i - i0)/dt, 1)} per min")
        if i in setprimes or i/2 in setprimes or i/3 in setprimes:
            continue
        fact1 = frozenset([tuple(ary) for ary in factorizations_outer(i)])
        for f1 in fact1:
            frac1 = calc_density(i, f1)
            if frac1 in setfractions:
                print(f"{f1} {i} {frac1}")
                if bbreak:
                    break
    
# 
# main loop
# 
def main():
    args = sys.argv[1:]
    imult = 32
    numcores = int(args[0])
    i0, i1 = int(args[1]) - numcores * imult, int(args[2])
    if i0 < 12:
        i0 = 12
    print(f"starting process with numcores={numcores}, istart={i0}, ifinish={i1}")
    i, t0 = i0, time.time()
    while i < i1:
        i += numcores * imult
        pr = [object(),] * numcores
        for p in range(0, numcores):
            pr[p] = Process(target=factors_loop, args=(t0, i0, i + p * imult, i + (p + 1) * imult, False))
            pr[p].start()
        for p in range(0, numcores):
            pr[p].join()
    

if __name__ == '__main__':
    main()



