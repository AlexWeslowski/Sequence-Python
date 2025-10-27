import subprocess
import sys

def install_packages(package_list):
    for package_name in package_list:
        try:
            is_git = package_name.startswith("git+") or package_name.find("https://") > 0
            if False:
                spec = importlib.util.find_spec(package_name)
                if spec is None:
                    raise ImportError(f"Package installed but module '{package_name}' is not found.")
            if is_git:
                _ = __import__(package_name[package_name.rfind("/")+1:package_name.rfind(".")].lower())
            else:
                _ = __import__(package_name)
            #eval(f"{package_name} = __import__('{package_name}')")
        except ImportError as ie:
            try:
                #pip.main(['install', package_name])
                process = subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True, capture_output=True, text=True)
                print(process.stdout)
                if not is_git:
                    _ = __import__(package_name)
            except subprocess.CalledProcessError as cpe:
                print(f"Exit Code: {cpe.returncode}")
                print("[STDOUT]")
                print(cpe.stdout) 
                print("[STDERR]")
                print(cpe.stderr) 
                pass
            except FileNotFoundError as fnfe:
                print("\nError: pip command or python executable was not found.")
                pass
            pass

package_list = "multiprocessing, math, numpy, numba, sympy, sparse, itertools, functools, operator, primefac, bitarray, numbers, operator, fractions, random, sqlite3, filelock, io, gzip, threading, queue, time, psutil, os, pathlib, platformdirs, traceback".split(", ")
package_list.append("git+https://github.com/AlexWeslowski/Divisors.git")
install_packages(package_list)

import multiprocessing, math, numpy, sparse, itertools, functools, operator, primefac, bitarray, numbers, operator, fractions, random, sqlite3, filelock, io, gzip, threading, queue, time, psutil, os, pathlib, platformdirs, traceback
import numba, numba.experimental, numba.extending, numba.typed, numba.types
import sympy, sympy.external.gmpy
from multiprocessing import Process
import divisors as d

MAX_RECURSION = 8
bln_cpp = True
bln_numba = True
bln_divisors = True
verbose = False

ap = 2**10
if bln_numba:
    aryprimes = numpy.array([False]*(ap+1), dtype=bool)
else:
    aryprimes = bitarray.bitarray(ap+1)
    aryprimes.setall(0)

def fill_primes(ap):
    global verbose
    global bln_numba
    global aryprimes
    if verbose: print(f"fill_primes({ap:,})")
    if bln_numba:
        aryprimes = numpy.array([False]*(ap+1), dtype=bool)
    else:
        aryprimes = bitarray.bitarray(ap+1)
        aryprimes.setall(0)
    try:
        import primesieve
        for p in primesieve.primes(ap+1):
            aryprimes[p] = True
    except ModuleNotFoundError as mnfe:
        for p in sympy.sieve.primerange(ap+1):
            aryprimes[p] = True
        pass

# 2**28 ~ 10**8.43
# 2**33 ~ 10**9.93
fill_primes(ap)


spec = [
    ('numerator', numba.int64),
    ('denominator', numba.int64)
]

@numba.experimental.jitclass(spec)
class Fraction():
    #__slots__ = ('numerator', 'denominator')
    
    def __init__(self, num, den):
        if num == 1:
            self.numerator = num
            self.denominator = den
        else:
            g = numpy.gcd(num, den)
            if den < 0:
                g = -g
            self.numerator = num//g
            self.denominator = den//g
    
    def __add__(self, b):
        na, da = self.numerator, self.denominator
        nb, db = b.numerator, b.denominator
        g1 = numpy.gcd(da, db)
        if g1 == 1:
            return Fraction(na * db + da * nb, da * db)
        s = da // g1
        t = na * (db // g1) + nb * s
        g2 = numpy.gcd(t, g1)
        if g2 == 1:
            return Fraction(t, s * db)
        return Fraction(t // g2, s * (db // g2))

    #__add__, __radd__ = _operator_fallbacks(_add, operator.add)

    def __sub__(self, b):
        na, da = self.numerator, self.denominator
        nb, db = b.numerator, b.denominator
        g1 = numpy.gcd(da, db)
        if g1 == 1:
            return Fraction(na * db - da * nb, da * db)
        s = da // g1
        t = na * (db // g1) - nb * s
        g2 = numpy.gcd(t, g1)
        if g2 == 1:
            return Fraction(t, s * db)
        return Fraction(t // g2, s * (db // g2))

    #__sub__, __rsub__ = _operator_fallbacks(_sub, operator.sub)
    
    def __mul__(self, b):
        na, da = self.numerator, self.denominator
        nb, db = b.numerator, b.denominator
        g1 = numpy.gcd(na, db)
        if g1 > 1:
            na //= g1
            db //= g1
        g2 = numpy.gcd(nb, da)
        if g2 > 1:
            nb //= g2
            da //= g2
        return Fraction(na * nb, db * da)

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        else:
            #return '%s/%s' % (self.numerator, self.denominator)
            return str(self.numerator) + "/" + str(self.denominator)
    
    def __lt__(a, b):
        return a.numerator * b.denominator < a.denominator * b.numerator

    def __gt__(a, b):
        return a.numerator * b.denominator > a.denominator * b.numerator

    def __le__(a, b):
        return a.numerator * b.denominator <= a.denominator * b.numerator

    def __ge__(a, b):
        return a.numerator * b.denominator >= a.denominator * b.numerator
    
    def __eq__(a, b):
        return a.numerator == b.numerator and a.numerator == b.denominator
    
    def __hash__(self):
        return hash((self.numerator, self.denominator))

setfractions = frozenset([Fraction(1, 2),])


def gcd_cached(i, j):
    global gcd_cache
    if gcd_cache[i][j] == 0:
        gcd_cache[i][j] = math.gcd(i, j)    
    return gcd_cache[i][j]

def gcd(tpl):
    if tpl[0] <= 12288 or tpl[1] <= 12288:
        return gcd_cached(tpl[0], tpl[1])
    return math.gcd(tpl[0], tpl[1])

def lcm_cached(i, j):
    global lcm_cache
    if lcm_cache[i][j] == 0:
        lcm_cache[i][j] = math.lcm(i, j)
    return lcm_cache[i][j]

def lcm(tpl):
    if tpl[0] <= 12288 or tpl[1] <= 12288:
        return lcm_cached(tpl[0], tpl[1])
    return math.lcm(tpl[0], tpl[1])


def lcm2(tpl):
    t1 = tpl[-1]
    for t2 in tpl[-2::-1]:
        t1 = math.lcm(t2, t1)
    return t1


@numba.jit(nopython=True)
def mult_numba(tpl):
    global aryprimes
    ary = list(tpl)
    ilen = len(ary)    
    if ilen <= 2:
        # ary[1] = ary[0]*ary[1] if aryprimes[ary[0]] or aryprimes[ary[1]] else ary[0]*ary[1]//numpy.gcd(ary[0], ary[1])
        ary[1] = ary[0]*ary[1] if aryprimes[ary[0]] or aryprimes[ary[1]] else numpy.lcm(ary[0], ary[1])
        return ary[1]
    else:
        # ary[1] = ary[0]*ary[1] if aryprimes[ary[0]] or aryprimes[ary[1]] else ary[0]*ary[1]//numpy.gcd(ary[0], ary[1])
        ary[1] = ary[0]*ary[1] if aryprimes[ary[0]] or aryprimes[ary[1]] else numpy.lcm(ary[0], ary[1])
        for a in range(2, ilen):
            # ary[a] = ary[a-1]*ary[a] if aryprimes[ary[a]] else ary[a-1]*ary[a]//numpy.gcd(ary[a-1], ary[a])
            ary[a] = ary[a-1]*ary[a] if aryprimes[ary[a]] else numpy.lcm(ary[a-1], ary[a])
            if ilen <= a + 1:
                return ary[a]

def mult(tpl):
    global aryprimes
    ary = list(tpl)
    ilen = len(ary)    
    if ilen <= 2:
        # ary[1] = ary[0]*ary[1] if aryprimes[ary[0]] or aryprimes[ary[1]] else ary[0]*ary[1]//numpy.gcd(ary[0], ary[1])
        ary[1] = ary[0]*ary[1] if aryprimes[ary[0]] or aryprimes[ary[1]] else numpy.lcm(ary[0], ary[1])
        return ary[1]
    else:
        # ary[1] = ary[0]*ary[1] if aryprimes[ary[0]] or aryprimes[ary[1]] else ary[0]*ary[1]//numpy.gcd(ary[0], ary[1])
        ary[1] = ary[0]*ary[1] if aryprimes[ary[0]] or aryprimes[ary[1]] else numpy.lcm(ary[0], ary[1])
        for a in range(2, ilen):
            # ary[a] = ary[a-1]*ary[a] if aryprimes[ary[a]] else ary[a-1]*ary[a]//numpy.gcd(ary[a-1], ary[a])
            ary[a] = ary[a-1]*ary[a] if aryprimes[ary[a]] else numpy.lcm(ary[a-1], ary[a])
            if ilen <= a + 1:
                return ary[a]


bcheckprime = False
max_sum = Fraction(1, 1) if bln_numba else fractions.Fraction(1, 1)
min_factors = 2
max_factors = 10
max_denominator = 3

#factorizations_outer(720)
#calc_density2(720, [5, 9, 16], max_sum)
@numba.jit(nopython=True)
def calc_density_numba(i, a, max_sum):
    #global bcheckprime
    #global aryprimes
    bcheckmax = False
    ilen = len(a)
    # if bcheckprime:
        # if ilen == 3 and aryprimes[a[0]] and aryprimes[a[1]] and aryprimes[a[2]]:
            # return Fraction(a[0] - 1, a[0]) * Fraction(a[1] - 1, a[1]) * Fraction(a[2] - 1, a[2])
        # if ilen == 4 and aryprimes[a[0]] and aryprimes[a[1]] and aryprimes[a[2]] and aryprimes[a[3]]:
            # return Fraction(a[0] - 1, a[0]) * Fraction(a[1] - 1, a[1]) * Fraction(a[2] - 1, a[2]) * Fraction(a[3] - 1, a[3])
        # if ilen == 5 and aryprimes[a[0]] and aryprimes[a[1]] and aryprimes[a[2]] and aryprimes[a[3]] and aryprimes[a[4]]:
            # return Fraction(a[0] - 1, a[0]) * Fraction(a[1] - 1, a[1]) * Fraction(a[2] - 1, a[2]) * Fraction(a[3] - 1, a[3]) * Fraction(a[4] - 1, a[4])
    frac = Fraction(1, a[0])
    if frac > max_sum:
        return Fraction(1, 1)
    frac += Fraction(1, a[1]) - Fraction(1, mult_numba(a[0:2]))
    if bcheckmax and frac > max_sum:
        return Fraction(1, 1)
    if ilen >= 3:
        frac += Fraction(1, a[2]) - Fraction(1, mult_numba((a[0], a[2]))) - Fraction(1, mult_numba((a[1], a[2]))) + Fraction(1, mult_numba(a[0:3]))
        if bcheckmax and frac > max_sum:
            return Fraction(1, 1)
    if ilen >= 4:
        frac += Fraction(1, a[3]) - Fraction(1, mult_numba((a[0], a[3]))) - Fraction(1, mult_numba((a[1], a[3]))) - Fraction(1, mult_numba((a[2], a[3]))) + Fraction(1, mult_numba((a[0], a[1], a[3]))) + Fraction(1, mult_numba((a[0], a[2], a[3]))) + Fraction(1, mult_numba((a[1], a[2], a[3]))) - Fraction(1, mult_numba(a[0:4]))
        if bcheckmax and frac > max_sum:
            return Fraction(1, 1)
    if ilen >= 5:
        frac += Fraction(1, a[4]) - Fraction(1, mult_numba((a[0], a[4]))) - Fraction(1, mult_numba((a[1], a[4]))) - Fraction(1, mult_numba((a[2], a[4]))) - Fraction(1, mult_numba((a[3], a[4]))) + Fraction(1, mult_numba((a[0], a[1], a[4]))) + Fraction(1, mult_numba((a[0], a[2], a[4]))) + Fraction(1, mult_numba((a[0], a[3], a[4]))) + Fraction(1, mult_numba((a[1], a[2], a[4]))) + Fraction(1, mult_numba((a[1], a[3], a[4]))) + Fraction(1, mult_numba((a[2], a[3], a[4]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4]))) + Fraction(1, mult_numba(a[0:5]))
        if bcheckmax and frac > max_sum:
            return Fraction(1, 1)
    if ilen >= 6:
        frac += Fraction(1, a[5]) - Fraction(1, mult_numba((a[0], a[5]))) - Fraction(1, mult_numba((a[1], a[5]))) - Fraction(1, mult_numba((a[2], a[5]))) - Fraction(1, mult_numba((a[3], a[5]))) - Fraction(1, mult_numba((a[4], a[5]))) + Fraction(1, mult_numba((a[0], a[1], a[5]))) + Fraction(1, mult_numba((a[0], a[2], a[5]))) + Fraction(1, mult_numba((a[0], a[3], a[5]))) + Fraction(1, mult_numba((a[0], a[4], a[5]))) + Fraction(1, mult_numba((a[1], a[2], a[5]))) + Fraction(1, mult_numba((a[1], a[3], a[5]))) + Fraction(1, mult_numba((a[1], a[4], a[5]))) + Fraction(1, mult_numba((a[2], a[3], a[5]))) + Fraction(1, mult_numba((a[2], a[4], a[5]))) + Fraction(1, mult_numba((a[3], a[4], a[5]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[5]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[5]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[5]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[5]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[5]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[5]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[5]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[5]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[5]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[5]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5]))) - Fraction(1, mult_numba(a[0:6]))
        if bcheckmax and frac > max_sum:
            return Fraction(1, 1)
    if ilen >= 7:
        frac += Fraction(1, a[6]) - Fraction(1, mult_numba((a[0], a[6]))) - Fraction(1, mult_numba((a[1], a[6]))) - Fraction(1, mult_numba((a[2], a[6]))) - Fraction(1, mult_numba((a[3], a[6]))) - Fraction(1, mult_numba((a[4], a[6]))) - Fraction(1, mult_numba((a[5], a[6]))) + Fraction(1, mult_numba((a[0], a[1], a[6]))) + Fraction(1, mult_numba((a[0], a[2], a[6]))) + Fraction(1, mult_numba((a[0], a[3], a[6]))) + Fraction(1, mult_numba((a[0], a[4], a[6]))) + Fraction(1, mult_numba((a[0], a[5], a[6]))) + Fraction(1, mult_numba((a[1], a[2], a[6]))) + Fraction(1, mult_numba((a[1], a[3], a[6]))) + Fraction(1, mult_numba((a[1], a[4], a[6]))) + Fraction(1, mult_numba((a[1], a[5], a[6]))) + Fraction(1, mult_numba((a[2], a[3], a[6]))) + Fraction(1, mult_numba((a[2], a[4], a[6]))) + Fraction(1, mult_numba((a[2], a[5], a[6]))) + Fraction(1, mult_numba((a[3], a[4], a[6]))) + Fraction(1, mult_numba((a[3], a[5], a[6]))) + Fraction(1, mult_numba((a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[6]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[6]))) - Fraction(1, mult_numba((a[0], a[2], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[6]))) - Fraction(1, mult_numba((a[0], a[3], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[6]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[6]))) - Fraction(1, mult_numba((a[1], a[2], a[5], a[6]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[6]))) - Fraction(1, mult_numba((a[1], a[3], a[5], a[6]))) - Fraction(1, mult_numba((a[1], a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[6]))) - Fraction(1, mult_numba((a[2], a[3], a[5], a[6]))) - Fraction(1, mult_numba((a[2], a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[3], a[4], a[5], a[6]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[6]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[6]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[5], a[6]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[6]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[5], a[6]))) + Fraction(1, mult_numba((a[0], a[1], a[4], a[5], a[6]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[6]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[5], a[6]))) + Fraction(1, mult_numba((a[0], a[2], a[4], a[5], a[6]))) + Fraction(1, mult_numba((a[0], a[3], a[4], a[5], a[6]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[6]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[5], a[6]))) + Fraction(1, mult_numba((a[1], a[2], a[4], a[5], a[6]))) + Fraction(1, mult_numba((a[1], a[3], a[4], a[5], a[6]))) + Fraction(1, mult_numba((a[2], a[3], a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5], a[6]))) + Fraction(1, mult_numba(a[0:7]))
        if bcheckmax and frac > max_sum:
            return Fraction(1, 1)
    if ilen >= 8:
        frac += Fraction(1, a[7]) - Fraction(1, mult_numba((a[0], a[7]))) - Fraction(1, mult_numba((a[1], a[7]))) - Fraction(1, mult_numba((a[2], a[7]))) - Fraction(1, mult_numba((a[3], a[7]))) - Fraction(1, mult_numba((a[4], a[7]))) - Fraction(1, mult_numba((a[5], a[7]))) - Fraction(1, mult_numba((a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[7]))) + Fraction(1, mult_numba((a[0], a[3], a[7]))) + Fraction(1, mult_numba((a[0], a[4], a[7]))) + Fraction(1, mult_numba((a[0], a[5], a[7]))) + Fraction(1, mult_numba((a[0], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[7]))) + Fraction(1, mult_numba((a[1], a[3], a[7]))) + Fraction(1, mult_numba((a[1], a[4], a[7]))) + Fraction(1, mult_numba((a[1], a[5], a[7]))) + Fraction(1, mult_numba((a[1], a[6], a[7]))) + Fraction(1, mult_numba((a[2], a[3], a[7]))) + Fraction(1, mult_numba((a[2], a[4], a[7]))) + Fraction(1, mult_numba((a[2], a[5], a[7]))) + Fraction(1, mult_numba((a[2], a[6], a[7]))) + Fraction(1, mult_numba((a[3], a[4], a[7]))) + Fraction(1, mult_numba((a[3], a[5], a[7]))) + Fraction(1, mult_numba((a[3], a[6], a[7]))) + Fraction(1, mult_numba((a[4], a[5], a[7]))) + Fraction(1, mult_numba((a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[7]))) - Fraction(1, mult_numba((a[0], a[3], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[3], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[5], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[7]))) - Fraction(1, mult_numba((a[1], a[3], a[5], a[7]))) - Fraction(1, mult_numba((a[1], a[3], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[1], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[7]))) - Fraction(1, mult_numba((a[2], a[3], a[5], a[7]))) - Fraction(1, mult_numba((a[2], a[3], a[6], a[7]))) - Fraction(1, mult_numba((a[2], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[2], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[2], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[3], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[3], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[3], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[5], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[5], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[4], a[5], a[7])))
        frac += Fraction(1, mult_numba((a[0], a[1], a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[5], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[4], a[5], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[3], a[4], a[5], a[7]))) + Fraction(1, mult_numba((a[0], a[3], a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[3], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[5], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[4], a[5], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[3], a[4], a[5], a[7]))) + Fraction(1, mult_numba((a[1], a[3], a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[3], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[2], a[3], a[4], a[5], a[7]))) + Fraction(1, mult_numba((a[2], a[3], a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[2], a[3], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[2], a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[5], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, mult_numba(a[0:8]))
        if bcheckmax and frac > max_sum:
            return Fraction(1, 1)
    if ilen >= 9:
        frac += Fraction(1, a[8]) - Fraction(1, mult_numba((a[0], a[8]))) - Fraction(1, mult_numba((a[1], a[8]))) - Fraction(1, mult_numba((a[2], a[8]))) - Fraction(1, mult_numba((a[3], a[8]))) - Fraction(1, mult_numba((a[4], a[8]))) - Fraction(1, mult_numba((a[5], a[8]))) - Fraction(1, mult_numba((a[6], a[8]))) - Fraction(1, mult_numba((a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[8]))) + Fraction(1, mult_numba((a[0], a[4], a[8]))) + Fraction(1, mult_numba((a[0], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[8]))) + Fraction(1, mult_numba((a[1], a[4], a[8]))) + Fraction(1, mult_numba((a[1], a[5], a[8]))) + Fraction(1, mult_numba((a[1], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[8]))) + Fraction(1, mult_numba((a[2], a[4], a[8]))) + Fraction(1, mult_numba((a[2], a[5], a[8]))) + Fraction(1, mult_numba((a[2], a[6], a[8]))) + Fraction(1, mult_numba((a[2], a[7], a[8]))) + Fraction(1, mult_numba((a[3], a[4], a[8]))) + Fraction(1, mult_numba((a[3], a[5], a[8]))) + Fraction(1, mult_numba((a[3], a[6], a[8]))) + Fraction(1, mult_numba((a[3], a[7], a[8]))) + Fraction(1, mult_numba((a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[5], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[5], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[1], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[5], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[6], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[2], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[2], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[2], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[3], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[3], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[3], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[3], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[3], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[3], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[5], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[2], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[6], a[8])))
        frac += Fraction(-1, mult_numba((a[0], a[1], a[2], a[3], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba(a[0:9]))
        if bcheckmax and frac > max_sum:
            return Fraction(1, 1)
    return frac
    

"""
import fractions
import sys
import os
import threading
import platformdirs
import pathlib
import importlib
sys.path.append('C:\\Users\\alex.weslowski\\Documents\\Python\\Sequence\\github')
import sequence_threads as seq
from sequence_threads import Int128
import divisors as div
import time

seq.fill_primes(2**21)
i = 1048578
c = div.Combinations(i)
c.backtrack(i, [])
c.removeAt(3)
list(seq.factorizations_outer(i, bln_remove_gt_half=False))

numbat1 = 0
numbat2 = 0
for i in range(2**20, 2**20 + 2**18 + 1):
    t1 = time.time()
    ary1 = [seq.calc_density_numba(i, f1, seq.max_sum) for f1 in seq.factorizations_outer(i, bln_remove_gt_half=False)]
    numbat1 += time.time() - t1
    t2 = time.time()
    ary2 = [seq.calc_density_numba2(i, f1, seq.max_sum) for f1 in seq.factorizations_outer(i, bln_remove_gt_half=False)]
    numbat2 += time.time() - t2
    ary1n = [x.numerator for x in ary1]
    ary2n = [x.numerator for x in ary2]
    ary1d = [x.denominator for x in ary1]
    ary2d = [x.denominator for x in ary2]
    if ary1n != ary2n or ary1d != ary2d:
        break

Fraction(1, a[2]) - Fraction(1, mult_numba((a[0], a[2]))) - Fraction(1, mult_numba((a[1], a[2]))) + Fraction(1, mult_numba(a[0:3]))
a = [2, 3, 174763]
b = seq.mult_numba((a[0], a[2]))
c = seq.mult_numba((a[1], a[2]))
d = seq.mult_numba(a[0:3])
a128 = Int128(a[2])
b128 = Int128(b)
c128 = Int128(c)
d128 = Int128(d)
seq.Fraction(a128*b128*c128 - a128*b128*d128 - a128*c128*d128 + b128*c128*d128, a128*b128*c128*d128)
seq.Fraction(a[2]*b*c - a[2]*b*d - a[2]*c*d + b*c*d, a[2]*b*c*d)

# 64051561204955364
a[2]*b*c - a[2]*b*d - a[2]*c*d + b*c*d
num = a128*b128*c128 - a128*b128*d128 - a128*c128*d128 + b128*c128*d128
numpy.int64(num.limbs[0]) + (numpy.int64(num.limbs[1]) << 31) + (num.limbs[2] << 62) + (num.limbs[3] << 93)
int(a128*b128*c128 - a128*b128*d128 - a128*c128*d128 + b128*c128*d128)

# 33581528972584842836196 # 2**74.83
a[2]*b*c*d
int(a128*b128*c128*d128)
den = a128*b128*c128*d128
int(den.limbs[0]) + (int(den.limbs[1]) << 31) + (int(den.limbs[2]) << 62) + (int(den.limbs[3]) << 93)

fractions.Fraction(64051561204955364, 33581528972584842836196)
Fraction(1, 524289)

"""
@numba.jit(nopython=True)
def calc_density_numba2(i, a, max_sum):
    bcheckmax = False
    ilen = len(a)
    frac = Fraction(1, a[0])
    if frac > max_sum:
        return Fraction(1, 1)
    # sympy.together("1/a - 1/b")
    frac += Fraction(mult_numba(a[0:2]) - a[1], a[1] * mult_numba(a[0:2]))
    if bcheckmax and frac > max_sum:
        return Fraction(1, 1)
    if ilen >= 3:
        # Fraction(1, a[2]) - Fraction(1, mult_numba((a[0], a[2]))) - Fraction(1, mult_numba((a[1], a[2]))) + Fraction(1, mult_numba(a[0:3]))
        # str(sympy.together("1/a - 1/b - 1/c + 1/d")).replace("a", "a[2]").replace(")/(", ", ")
        b = mult_numba((a[0], a[2]))
        c = mult_numba((a[1], a[2]))
        d = mult_numba(a[0:3])
        frac += Fraction(a[2]*b*c - a[2]*b*d - a[2]*c*d + b*c*d, a[2]*b*c*d)
        if bcheckmax and frac > max_sum:
            return Fraction(1, 1)
    if ilen >= 4:
        # print("\n".join([f"{chr(98 + idx)} = mult_numba((a[{tpl[0]}], a[3]))" for idx, tpl in enumerate(itertools.combinations(range(3), 1))]))
        # print("\n".join([f"{chr(101 + idx)} = mult_numba((a[{tpl[0]}], a[{tpl[1]}], a[3]))" for idx, tpl in enumerate(itertools.combinations(range(3), 2))]))
        # str(sympy.together("1/a - 1/b - 1/c - 1/d + 1/e + 1/f + 1/g - 1/h")).replace("a", "a[3]").replace(")/(", ", ")
        b = mult_numba((a[0], a[3]))
        c = mult_numba((a[1], a[3]))
        d = mult_numba((a[2], a[3]))
        e = mult_numba((a[0], a[1], a[3]))
        f = mult_numba((a[0], a[2], a[3]))
        g = mult_numba((a[1], a[2], a[3]))
        h = mult_numba(a[0:4])
        frac += Fraction(-a[3]*b*c*d*e*f*g + a[3]*b*c*d*e*f*h + a[3]*b*c*d*e*g*h + a[3]*b*c*d*f*g*h - a[3]*b*c*e*f*g*h - a[3]*b*d*e*f*g*h - a[3]*c*d*e*f*g*h + b*c*d*e*f*g*h, a[3]*b*c*d*e*f*g*h)
        if bcheckmax and frac > max_sum:
            return Fraction(1, 1)
    if ilen >= 5:
        # print("\n".join([f"{chr(98 + idx)} = mult_numba((a[{tpl[0]}], a[4]))" for idx, tpl in enumerate(itertools.combinations(range(4), 1))]))
        # print("\n".join([f"{chr(102 + idx)} = mult_numba((a[{tpl[0]}], a[{tpl[1]}], a[4]))" for idx, tpl in enumerate(itertools.combinations(range(4), 2))]))
        # print("\n".join([f"{chr(108 + idx)} = mult_numba((a[{tpl[0]}], a[{tpl[1]}], a[{tpl[2]}], a[4]))" for idx, tpl in enumerate(itertools.combinations(range(4), 3))]))
        # str(sympy.together("1/a - " + " - ".join([f"1/{chr(98+i)}" for i in range(4)]) + " + " + " + ".join([f"1/{chr(102+i)}" for i in range(6)]) + " - " + " - ".join([f"1/{chr(108+i)}" for i in range(4)]) + f" + 1/{chr(112)}")).replace("a", "a[4]").replace(")/(", ", ")
        b = mult_numba((a[0], a[4]))
        c = mult_numba((a[1], a[4]))
        d = mult_numba((a[2], a[4]))
        e = mult_numba((a[3], a[4]))
        f = mult_numba((a[0], a[1], a[4]))
        g = mult_numba((a[0], a[2], a[4]))
        h = mult_numba((a[0], a[3], a[4]))
        i = mult_numba((a[1], a[2], a[4]))
        j = mult_numba((a[1], a[3], a[4]))
        k = mult_numba((a[2], a[3], a[4]))
        l = mult_numba((a[0], a[1], a[2], a[4]))
        m = mult_numba((a[0], a[1], a[3], a[4]))
        n = mult_numba((a[0], a[2], a[3], a[4]))
        o = mult_numba((a[1], a[2], a[3], a[4]))
        p = mult_numba(a[0:5])
        frac += Fraction(a[4]*b*c*d*e*f*g*h*i*j*k*l*m*n*o - a[4]*b*c*d*e*f*g*h*i*j*k*l*m*n*p - a[4]*b*c*d*e*f*g*h*i*j*k*l*m*o*p - a[4]*b*c*d*e*f*g*h*i*j*k*l*n*o*p - a[4]*b*c*d*e*f*g*h*i*j*k*m*n*o*p + a[4]*b*c*d*e*f*g*h*i*j*l*m*n*o*p + a[4]*b*c*d*e*f*g*h*i*k*l*m*n*o*p + a[4]*b*c*d*e*f*g*h*j*k*l*m*n*o*p + a[4]*b*c*d*e*f*g*i*j*k*l*m*n*o*p + a[4]*b*c*d*e*f*h*i*j*k*l*m*n*o*p + a[4]*b*c*d*e*g*h*i*j*k*l*m*n*o*p - a[4]*b*c*d*f*g*h*i*j*k*l*m*n*o*p - a[4]*b*c*e*f*g*h*i*j*k*l*m*n*o*p - a[4]*b*d*e*f*g*h*i*j*k*l*m*n*o*p - a[4]*c*d*e*f*g*h*i*j*k*l*m*n*o*p + b*c*d*e*f*g*h*i*j*k*l*m*n*o*p, a[4]*b*c*d*e*f*g*h*i*j*k*l*m*n*o*p)
        if bcheckmax and frac > max_sum:
            return Fraction(1, 1)
    if ilen >= 6:
        frac += Fraction(1, a[5]) - Fraction(1, mult_numba((a[0], a[5]))) - Fraction(1, mult_numba((a[1], a[5]))) - Fraction(1, mult_numba((a[2], a[5]))) - Fraction(1, mult_numba((a[3], a[5]))) - Fraction(1, mult_numba((a[4], a[5]))) + Fraction(1, mult_numba((a[0], a[1], a[5]))) + Fraction(1, mult_numba((a[0], a[2], a[5]))) + Fraction(1, mult_numba((a[0], a[3], a[5]))) + Fraction(1, mult_numba((a[0], a[4], a[5]))) + Fraction(1, mult_numba((a[1], a[2], a[5]))) + Fraction(1, mult_numba((a[1], a[3], a[5]))) + Fraction(1, mult_numba((a[1], a[4], a[5]))) + Fraction(1, mult_numba((a[2], a[3], a[5]))) + Fraction(1, mult_numba((a[2], a[4], a[5]))) + Fraction(1, mult_numba((a[3], a[4], a[5]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[5]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[5]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[5]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[5]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[5]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[5]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[5]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[5]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[5]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[5]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5]))) - Fraction(1, mult_numba(a[0:6]))
        if bcheckmax and frac > max_sum:
            return Fraction(1, 1)
    if ilen >= 7:
        frac += Fraction(1, a[6]) - Fraction(1, mult_numba((a[0], a[6]))) - Fraction(1, mult_numba((a[1], a[6]))) - Fraction(1, mult_numba((a[2], a[6]))) - Fraction(1, mult_numba((a[3], a[6]))) - Fraction(1, mult_numba((a[4], a[6]))) - Fraction(1, mult_numba((a[5], a[6]))) + Fraction(1, mult_numba((a[0], a[1], a[6]))) + Fraction(1, mult_numba((a[0], a[2], a[6]))) + Fraction(1, mult_numba((a[0], a[3], a[6]))) + Fraction(1, mult_numba((a[0], a[4], a[6]))) + Fraction(1, mult_numba((a[0], a[5], a[6]))) + Fraction(1, mult_numba((a[1], a[2], a[6]))) + Fraction(1, mult_numba((a[1], a[3], a[6]))) + Fraction(1, mult_numba((a[1], a[4], a[6]))) + Fraction(1, mult_numba((a[1], a[5], a[6]))) + Fraction(1, mult_numba((a[2], a[3], a[6]))) + Fraction(1, mult_numba((a[2], a[4], a[6]))) + Fraction(1, mult_numba((a[2], a[5], a[6]))) + Fraction(1, mult_numba((a[3], a[4], a[6]))) + Fraction(1, mult_numba((a[3], a[5], a[6]))) + Fraction(1, mult_numba((a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[6]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[6]))) - Fraction(1, mult_numba((a[0], a[2], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[6]))) - Fraction(1, mult_numba((a[0], a[3], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[6]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[6]))) - Fraction(1, mult_numba((a[1], a[2], a[5], a[6]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[6]))) - Fraction(1, mult_numba((a[1], a[3], a[5], a[6]))) - Fraction(1, mult_numba((a[1], a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[6]))) - Fraction(1, mult_numba((a[2], a[3], a[5], a[6]))) - Fraction(1, mult_numba((a[2], a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[3], a[4], a[5], a[6]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[6]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[6]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[5], a[6]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[6]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[5], a[6]))) + Fraction(1, mult_numba((a[0], a[1], a[4], a[5], a[6]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[6]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[5], a[6]))) + Fraction(1, mult_numba((a[0], a[2], a[4], a[5], a[6]))) + Fraction(1, mult_numba((a[0], a[3], a[4], a[5], a[6]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[6]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[5], a[6]))) + Fraction(1, mult_numba((a[1], a[2], a[4], a[5], a[6]))) + Fraction(1, mult_numba((a[1], a[3], a[4], a[5], a[6]))) + Fraction(1, mult_numba((a[2], a[3], a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5], a[6]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5], a[6]))) + Fraction(1, mult_numba(a[0:7]))
        if bcheckmax and frac > max_sum:
            return Fraction(1, 1)
    if ilen >= 8:
        frac += Fraction(1, a[7]) - Fraction(1, mult_numba((a[0], a[7]))) - Fraction(1, mult_numba((a[1], a[7]))) - Fraction(1, mult_numba((a[2], a[7]))) - Fraction(1, mult_numba((a[3], a[7]))) - Fraction(1, mult_numba((a[4], a[7]))) - Fraction(1, mult_numba((a[5], a[7]))) - Fraction(1, mult_numba((a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[7]))) + Fraction(1, mult_numba((a[0], a[3], a[7]))) + Fraction(1, mult_numba((a[0], a[4], a[7]))) + Fraction(1, mult_numba((a[0], a[5], a[7]))) + Fraction(1, mult_numba((a[0], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[7]))) + Fraction(1, mult_numba((a[1], a[3], a[7]))) + Fraction(1, mult_numba((a[1], a[4], a[7]))) + Fraction(1, mult_numba((a[1], a[5], a[7]))) + Fraction(1, mult_numba((a[1], a[6], a[7]))) + Fraction(1, mult_numba((a[2], a[3], a[7]))) + Fraction(1, mult_numba((a[2], a[4], a[7]))) + Fraction(1, mult_numba((a[2], a[5], a[7]))) + Fraction(1, mult_numba((a[2], a[6], a[7]))) + Fraction(1, mult_numba((a[3], a[4], a[7]))) + Fraction(1, mult_numba((a[3], a[5], a[7]))) + Fraction(1, mult_numba((a[3], a[6], a[7]))) + Fraction(1, mult_numba((a[4], a[5], a[7]))) + Fraction(1, mult_numba((a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[7]))) - Fraction(1, mult_numba((a[0], a[3], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[3], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[5], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[7]))) - Fraction(1, mult_numba((a[1], a[3], a[5], a[7]))) - Fraction(1, mult_numba((a[1], a[3], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[1], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[7]))) - Fraction(1, mult_numba((a[2], a[3], a[5], a[7]))) - Fraction(1, mult_numba((a[2], a[3], a[6], a[7]))) - Fraction(1, mult_numba((a[2], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[2], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[2], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[3], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[3], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[3], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[5], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[5], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[4], a[5], a[7])))
        frac += Fraction(1, mult_numba((a[0], a[1], a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[5], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[4], a[5], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[3], a[4], a[5], a[7]))) + Fraction(1, mult_numba((a[0], a[3], a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[3], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[5], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[4], a[5], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[3], a[4], a[5], a[7]))) + Fraction(1, mult_numba((a[1], a[3], a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[3], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[2], a[3], a[4], a[5], a[7]))) + Fraction(1, mult_numba((a[2], a[3], a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[2], a[3], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[2], a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[5], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5], a[6], a[7]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5], a[6], a[7]))) - Fraction(1, mult_numba(a[0:8]))
        if bcheckmax and frac > max_sum:
            return Fraction(1, 1)
    if ilen >= 9:
        frac += Fraction(1, a[8]) - Fraction(1, mult_numba((a[0], a[8]))) - Fraction(1, mult_numba((a[1], a[8]))) - Fraction(1, mult_numba((a[2], a[8]))) - Fraction(1, mult_numba((a[3], a[8]))) - Fraction(1, mult_numba((a[4], a[8]))) - Fraction(1, mult_numba((a[5], a[8]))) - Fraction(1, mult_numba((a[6], a[8]))) - Fraction(1, mult_numba((a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[8]))) + Fraction(1, mult_numba((a[0], a[4], a[8]))) + Fraction(1, mult_numba((a[0], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[8]))) + Fraction(1, mult_numba((a[1], a[4], a[8]))) + Fraction(1, mult_numba((a[1], a[5], a[8]))) + Fraction(1, mult_numba((a[1], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[8]))) + Fraction(1, mult_numba((a[2], a[4], a[8]))) + Fraction(1, mult_numba((a[2], a[5], a[8]))) + Fraction(1, mult_numba((a[2], a[6], a[8]))) + Fraction(1, mult_numba((a[2], a[7], a[8]))) + Fraction(1, mult_numba((a[3], a[4], a[8]))) + Fraction(1, mult_numba((a[3], a[5], a[8]))) + Fraction(1, mult_numba((a[3], a[6], a[8]))) + Fraction(1, mult_numba((a[3], a[7], a[8]))) + Fraction(1, mult_numba((a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[5], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[5], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[1], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[5], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[6], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[2], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[2], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[2], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[3], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[3], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[3], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[3], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[3], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[3], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[5], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[2], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[6], a[8])))
        frac += Fraction(-1, mult_numba((a[0], a[1], a[2], a[3], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[2], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[5], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[2], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[1], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[2], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[0], a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5], a[6], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[3], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[2], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[1], a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba((a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[5], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[4], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[3], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[2], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[1], a[3], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[0], a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) - Fraction(1, mult_numba((a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) + Fraction(1, mult_numba(a[0:9]))
        if bcheckmax and frac > max_sum:
            return Fraction(1, 1)
    return frac


def calc_density_python(i, a, max_sum):
    bcheckmax = False
    ilen = len(a)
    frac = fractions.Fraction(1, a[0])
    if frac > max_sum:
        return fractions.Fraction(1, 1)
    frac += fractions.Fraction(1, a[1]) - fractions.Fraction(1, mult(a[0:2]))
    if bcheckmax and frac > max_sum:
        return fractions.Fraction(1, 1)
    if ilen >= 3:
        frac += fractions.Fraction(1, a[2]) - fractions.Fraction(1, mult((a[0], a[2]))) - fractions.Fraction(1, mult((a[1], a[2]))) + fractions.Fraction(1, mult(a[0:3]))
        if bcheckmax and frac > max_sum:
            return fractions.Fraction(1, 1)
    if ilen >= 4:
        frac += fractions.Fraction(1, a[3]) - fractions.Fraction(1, mult((a[0], a[3]))) - fractions.Fraction(1, mult((a[1], a[3]))) - fractions.Fraction(1, mult((a[2], a[3]))) + fractions.Fraction(1, mult((a[0], a[1], a[3]))) + fractions.Fraction(1, mult((a[0], a[2], a[3]))) + fractions.Fraction(1, mult((a[1], a[2], a[3]))) - fractions.Fraction(1, mult(a[0:4]))
        if bcheckmax and frac > max_sum:
            return fractions.Fraction(1, 1)
    if ilen >= 5:
        frac += fractions.Fraction(1, a[4]) - fractions.Fraction(1, mult((a[0], a[4]))) - fractions.Fraction(1, mult((a[1], a[4]))) - fractions.Fraction(1, mult((a[2], a[4]))) - fractions.Fraction(1, mult((a[3], a[4]))) + fractions.Fraction(1, mult((a[0], a[1], a[4]))) + fractions.Fraction(1, mult((a[0], a[2], a[4]))) + fractions.Fraction(1, mult((a[0], a[3], a[4]))) + fractions.Fraction(1, mult((a[1], a[2], a[4]))) + fractions.Fraction(1, mult((a[1], a[3], a[4]))) + fractions.Fraction(1, mult((a[2], a[3], a[4]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[4]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[4]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[4]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[4]))) + fractions.Fraction(1, mult(a[0:5]))
        if bcheckmax and frac > max_sum:
            return fractions.Fraction(1, 1)
    if ilen >= 6:
        frac += fractions.Fraction(1, a[5]) - fractions.Fraction(1, mult((a[0], a[5]))) - fractions.Fraction(1, mult((a[1], a[5]))) - fractions.Fraction(1, mult((a[2], a[5]))) - fractions.Fraction(1, mult((a[3], a[5]))) - fractions.Fraction(1, mult((a[4], a[5]))) + fractions.Fraction(1, mult((a[0], a[1], a[5]))) + fractions.Fraction(1, mult((a[0], a[2], a[5]))) + fractions.Fraction(1, mult((a[0], a[3], a[5]))) + fractions.Fraction(1, mult((a[0], a[4], a[5]))) + fractions.Fraction(1, mult((a[1], a[2], a[5]))) + fractions.Fraction(1, mult((a[1], a[3], a[5]))) + fractions.Fraction(1, mult((a[1], a[4], a[5]))) + fractions.Fraction(1, mult((a[2], a[3], a[5]))) + fractions.Fraction(1, mult((a[2], a[4], a[5]))) + fractions.Fraction(1, mult((a[3], a[4], a[5]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[5]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[5]))) - fractions.Fraction(1, mult((a[0], a[1], a[4], a[5]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[5]))) - fractions.Fraction(1, mult((a[0], a[2], a[4], a[5]))) - fractions.Fraction(1, mult((a[0], a[3], a[4], a[5]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[5]))) - fractions.Fraction(1, mult((a[1], a[2], a[4], a[5]))) - fractions.Fraction(1, mult((a[1], a[3], a[4], a[5]))) - fractions.Fraction(1, mult((a[2], a[3], a[4], a[5]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[5]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[5]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[5]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[5]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[5]))) - fractions.Fraction(1, mult(a[0:6]))
        if bcheckmax and frac > max_sum:
            return fractions.Fraction(1, 1)
    if ilen >= 7:
        frac += fractions.Fraction(1, a[6]) - fractions.Fraction(1, mult((a[0], a[6]))) - fractions.Fraction(1, mult((a[1], a[6]))) - fractions.Fraction(1, mult((a[2], a[6]))) - fractions.Fraction(1, mult((a[3], a[6]))) - fractions.Fraction(1, mult((a[4], a[6]))) - fractions.Fraction(1, mult((a[5], a[6]))) + fractions.Fraction(1, mult((a[0], a[1], a[6]))) + fractions.Fraction(1, mult((a[0], a[2], a[6]))) + fractions.Fraction(1, mult((a[0], a[3], a[6]))) + fractions.Fraction(1, mult((a[0], a[4], a[6]))) + fractions.Fraction(1, mult((a[0], a[5], a[6]))) + fractions.Fraction(1, mult((a[1], a[2], a[6]))) + fractions.Fraction(1, mult((a[1], a[3], a[6]))) + fractions.Fraction(1, mult((a[1], a[4], a[6]))) + fractions.Fraction(1, mult((a[1], a[5], a[6]))) + fractions.Fraction(1, mult((a[2], a[3], a[6]))) + fractions.Fraction(1, mult((a[2], a[4], a[6]))) + fractions.Fraction(1, mult((a[2], a[5], a[6]))) + fractions.Fraction(1, mult((a[3], a[4], a[6]))) + fractions.Fraction(1, mult((a[3], a[5], a[6]))) + fractions.Fraction(1, mult((a[4], a[5], a[6]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[6]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[6]))) - fractions.Fraction(1, mult((a[0], a[1], a[4], a[6]))) - fractions.Fraction(1, mult((a[0], a[1], a[5], a[6]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[6]))) - fractions.Fraction(1, mult((a[0], a[2], a[4], a[6]))) - fractions.Fraction(1, mult((a[0], a[2], a[5], a[6]))) - fractions.Fraction(1, mult((a[0], a[3], a[4], a[6]))) - fractions.Fraction(1, mult((a[0], a[3], a[5], a[6]))) - fractions.Fraction(1, mult((a[0], a[4], a[5], a[6]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[6]))) - fractions.Fraction(1, mult((a[1], a[2], a[4], a[6]))) - fractions.Fraction(1, mult((a[1], a[2], a[5], a[6]))) - fractions.Fraction(1, mult((a[1], a[3], a[4], a[6]))) - fractions.Fraction(1, mult((a[1], a[3], a[5], a[6]))) - fractions.Fraction(1, mult((a[1], a[4], a[5], a[6]))) - fractions.Fraction(1, mult((a[2], a[3], a[4], a[6]))) - fractions.Fraction(1, mult((a[2], a[3], a[5], a[6]))) - fractions.Fraction(1, mult((a[2], a[4], a[5], a[6]))) - fractions.Fraction(1, mult((a[3], a[4], a[5], a[6]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[6]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[6]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[5], a[6]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[6]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[5], a[6]))) + fractions.Fraction(1, mult((a[0], a[1], a[4], a[5], a[6]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[6]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[5], a[6]))) + fractions.Fraction(1, mult((a[0], a[2], a[4], a[5], a[6]))) + fractions.Fraction(1, mult((a[0], a[3], a[4], a[5], a[6]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[6]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[5], a[6]))) + fractions.Fraction(1, mult((a[1], a[2], a[4], a[5], a[6]))) + fractions.Fraction(1, mult((a[1], a[3], a[4], a[5], a[6]))) + fractions.Fraction(1, mult((a[2], a[3], a[4], a[5], a[6]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[6]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[5], a[6]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[5], a[6]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[5], a[6]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[5], a[6]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[5], a[6]))) + fractions.Fraction(1, mult(a[0:7]))
        if bcheckmax and frac > max_sum:
            return fractions.Fraction(1, 1)
    if ilen >= 8:
        frac += fractions.Fraction(1, a[7]) - fractions.Fraction(1, mult((a[0], a[7]))) - fractions.Fraction(1, mult((a[1], a[7]))) - fractions.Fraction(1, mult((a[2], a[7]))) - fractions.Fraction(1, mult((a[3], a[7]))) - fractions.Fraction(1, mult((a[4], a[7]))) - fractions.Fraction(1, mult((a[5], a[7]))) - fractions.Fraction(1, mult((a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[7]))) + fractions.Fraction(1, mult((a[0], a[2], a[7]))) + fractions.Fraction(1, mult((a[0], a[3], a[7]))) + fractions.Fraction(1, mult((a[0], a[4], a[7]))) + fractions.Fraction(1, mult((a[0], a[5], a[7]))) + fractions.Fraction(1, mult((a[0], a[6], a[7]))) + fractions.Fraction(1, mult((a[1], a[2], a[7]))) + fractions.Fraction(1, mult((a[1], a[3], a[7]))) + fractions.Fraction(1, mult((a[1], a[4], a[7]))) + fractions.Fraction(1, mult((a[1], a[5], a[7]))) + fractions.Fraction(1, mult((a[1], a[6], a[7]))) + fractions.Fraction(1, mult((a[2], a[3], a[7]))) + fractions.Fraction(1, mult((a[2], a[4], a[7]))) + fractions.Fraction(1, mult((a[2], a[5], a[7]))) + fractions.Fraction(1, mult((a[2], a[6], a[7]))) + fractions.Fraction(1, mult((a[3], a[4], a[7]))) + fractions.Fraction(1, mult((a[3], a[5], a[7]))) + fractions.Fraction(1, mult((a[3], a[6], a[7]))) + fractions.Fraction(1, mult((a[4], a[5], a[7]))) + fractions.Fraction(1, mult((a[4], a[6], a[7]))) + fractions.Fraction(1, mult((a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[4], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[5], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[7]))) - fractions.Fraction(1, mult((a[0], a[2], a[4], a[7]))) - fractions.Fraction(1, mult((a[0], a[2], a[5], a[7]))) - fractions.Fraction(1, mult((a[0], a[2], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[3], a[4], a[7]))) - fractions.Fraction(1, mult((a[0], a[3], a[5], a[7]))) - fractions.Fraction(1, mult((a[0], a[3], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[4], a[5], a[7]))) - fractions.Fraction(1, mult((a[0], a[4], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[7]))) - fractions.Fraction(1, mult((a[1], a[2], a[4], a[7]))) - fractions.Fraction(1, mult((a[1], a[2], a[5], a[7]))) - fractions.Fraction(1, mult((a[1], a[2], a[6], a[7]))) - fractions.Fraction(1, mult((a[1], a[3], a[4], a[7]))) - fractions.Fraction(1, mult((a[1], a[3], a[5], a[7]))) - fractions.Fraction(1, mult((a[1], a[3], a[6], a[7]))) - fractions.Fraction(1, mult((a[1], a[4], a[5], a[7]))) - fractions.Fraction(1, mult((a[1], a[4], a[6], a[7]))) - fractions.Fraction(1, mult((a[1], a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[2], a[3], a[4], a[7]))) - fractions.Fraction(1, mult((a[2], a[3], a[5], a[7]))) - fractions.Fraction(1, mult((a[2], a[3], a[6], a[7]))) - fractions.Fraction(1, mult((a[2], a[4], a[5], a[7]))) - fractions.Fraction(1, mult((a[2], a[4], a[6], a[7]))) - fractions.Fraction(1, mult((a[2], a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[3], a[4], a[5], a[7]))) - fractions.Fraction(1, mult((a[3], a[4], a[6], a[7]))) - fractions.Fraction(1, mult((a[3], a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[4], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[5], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[5], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[4], a[5], a[7])))
        frac += fractions.Fraction(1, mult((a[0], a[1], a[4], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[7]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[5], a[7]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[2], a[4], a[5], a[7]))) + fractions.Fraction(1, mult((a[0], a[2], a[4], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[2], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[3], a[4], a[5], a[7]))) + fractions.Fraction(1, mult((a[0], a[3], a[4], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[3], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[4], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[7]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[5], a[7]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[6], a[7]))) + fractions.Fraction(1, mult((a[1], a[2], a[4], a[5], a[7]))) + fractions.Fraction(1, mult((a[1], a[2], a[4], a[6], a[7]))) + fractions.Fraction(1, mult((a[1], a[2], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[1], a[3], a[4], a[5], a[7]))) + fractions.Fraction(1, mult((a[1], a[3], a[4], a[6], a[7]))) + fractions.Fraction(1, mult((a[1], a[3], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[1], a[4], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[2], a[3], a[4], a[5], a[7]))) + fractions.Fraction(1, mult((a[2], a[3], a[4], a[6], a[7]))) + fractions.Fraction(1, mult((a[2], a[3], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[2], a[4], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[3], a[4], a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[5], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[5], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[5], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[1], a[4], a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[5], a[7]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[2], a[4], a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[0], a[3], a[4], a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[5], a[7]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[6], a[7]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[1], a[2], a[4], a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[1], a[3], a[4], a[5], a[6], a[7]))) - fractions.Fraction(1, mult((a[2], a[3], a[4], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[5], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[5], a[6], a[7]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[5], a[6], a[7]))) - fractions.Fraction(1, mult(a[0:8]))
        if bcheckmax and frac > max_sum:
            return fractions.Fraction(1, 1)
    if ilen >= 9:
        frac += fractions.Fraction(1, a[8]) - fractions.Fraction(1, mult((a[0], a[8]))) - fractions.Fraction(1, mult((a[1], a[8]))) - fractions.Fraction(1, mult((a[2], a[8]))) - fractions.Fraction(1, mult((a[3], a[8]))) - fractions.Fraction(1, mult((a[4], a[8]))) - fractions.Fraction(1, mult((a[5], a[8]))) - fractions.Fraction(1, mult((a[6], a[8]))) - fractions.Fraction(1, mult((a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[8]))) + fractions.Fraction(1, mult((a[0], a[3], a[8]))) + fractions.Fraction(1, mult((a[0], a[4], a[8]))) + fractions.Fraction(1, mult((a[0], a[5], a[8]))) + fractions.Fraction(1, mult((a[0], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[8]))) + fractions.Fraction(1, mult((a[1], a[3], a[8]))) + fractions.Fraction(1, mult((a[1], a[4], a[8]))) + fractions.Fraction(1, mult((a[1], a[5], a[8]))) + fractions.Fraction(1, mult((a[1], a[6], a[8]))) + fractions.Fraction(1, mult((a[1], a[7], a[8]))) + fractions.Fraction(1, mult((a[2], a[3], a[8]))) + fractions.Fraction(1, mult((a[2], a[4], a[8]))) + fractions.Fraction(1, mult((a[2], a[5], a[8]))) + fractions.Fraction(1, mult((a[2], a[6], a[8]))) + fractions.Fraction(1, mult((a[2], a[7], a[8]))) + fractions.Fraction(1, mult((a[3], a[4], a[8]))) + fractions.Fraction(1, mult((a[3], a[5], a[8]))) + fractions.Fraction(1, mult((a[3], a[6], a[8]))) + fractions.Fraction(1, mult((a[3], a[7], a[8]))) + fractions.Fraction(1, mult((a[4], a[5], a[8]))) + fractions.Fraction(1, mult((a[4], a[6], a[8]))) + fractions.Fraction(1, mult((a[4], a[7], a[8]))) + fractions.Fraction(1, mult((a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[4], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[5], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[4], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[5], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[3], a[4], a[8]))) - fractions.Fraction(1, mult((a[0], a[3], a[5], a[8]))) - fractions.Fraction(1, mult((a[0], a[3], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[3], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[4], a[5], a[8]))) - fractions.Fraction(1, mult((a[0], a[4], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[4], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[4], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[5], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[6], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[3], a[4], a[8]))) - fractions.Fraction(1, mult((a[1], a[3], a[5], a[8]))) - fractions.Fraction(1, mult((a[1], a[3], a[6], a[8]))) - fractions.Fraction(1, mult((a[1], a[3], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[4], a[5], a[8]))) - fractions.Fraction(1, mult((a[1], a[4], a[6], a[8]))) - fractions.Fraction(1, mult((a[1], a[4], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[1], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[2], a[3], a[4], a[8]))) - fractions.Fraction(1, mult((a[2], a[3], a[5], a[8]))) - fractions.Fraction(1, mult((a[2], a[3], a[6], a[8]))) - fractions.Fraction(1, mult((a[2], a[3], a[7], a[8]))) - fractions.Fraction(1, mult((a[2], a[4], a[5], a[8]))) - fractions.Fraction(1, mult((a[2], a[4], a[6], a[8]))) - fractions.Fraction(1, mult((a[2], a[4], a[7], a[8]))) - fractions.Fraction(1, mult((a[2], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[2], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[2], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[3], a[4], a[5], a[8]))) - fractions.Fraction(1, mult((a[3], a[4], a[6], a[8]))) - fractions.Fraction(1, mult((a[3], a[4], a[7], a[8]))) - fractions.Fraction(1, mult((a[3], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[3], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[3], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[4], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[4], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[4], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[5], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[5], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[4], a[5], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[4], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[4], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[5], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[4], a[5], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[4], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[4], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[3], a[4], a[5], a[8]))) + fractions.Fraction(1, mult((a[0], a[3], a[4], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[3], a[4], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[3], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[3], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[3], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[4], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[4], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[4], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[5], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[6], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[4], a[5], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[4], a[6], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[4], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[3], a[4], a[5], a[8]))) + fractions.Fraction(1, mult((a[1], a[3], a[4], a[6], a[8]))) + fractions.Fraction(1, mult((a[1], a[3], a[4], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[3], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[1], a[3], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[3], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[4], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[1], a[4], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[4], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[2], a[3], a[4], a[5], a[8]))) + fractions.Fraction(1, mult((a[2], a[3], a[4], a[6], a[8]))) + fractions.Fraction(1, mult((a[2], a[3], a[4], a[7], a[8]))) + fractions.Fraction(1, mult((a[2], a[3], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[2], a[3], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[2], a[3], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[2], a[4], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[2], a[4], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[2], a[4], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[2], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[3], a[4], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[3], a[4], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[3], a[4], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[3], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[4], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[5], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[6], a[8])))
        frac += fractions.Fraction(-1, mult((a[0], a[1], a[2], a[3], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[5], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[5], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[4], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[4], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[4], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[5], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[4], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[4], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[4], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[3], a[4], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[3], a[4], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[3], a[4], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[3], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[4], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[5], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[6], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[4], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[4], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[4], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[3], a[4], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[1], a[3], a[4], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[3], a[4], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[3], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[4], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[2], a[3], a[4], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[2], a[3], a[4], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[2], a[3], a[4], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[2], a[3], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[2], a[4], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[3], a[4], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[5], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[2], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[3], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[1], a[4], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[3], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[2], a[4], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[0], a[3], a[4], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[5], a[6], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[5], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[3], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[2], a[4], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[1], a[3], a[4], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult((a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[5], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[4], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[3], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[2], a[4], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[1], a[3], a[4], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[0], a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) - fractions.Fraction(1, mult((a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8]))) + fractions.Fraction(1, mult(a[0:9]))
        if bcheckmax and frac > max_sum:
            return fractions.Fraction(1, 1)
    return frac


bln_count = False
hsh_count_all = {}
hsh_count_prime = {}

#calc_density1(720, [5, 9, 16])
def calc_density1(i, a):
    global verbose
    global bln_count
    global bln_numba
    global hsh_count_all
    global hsh_count_prime
    global max_sum
    global total_calc_density
    if verbose: print(f"calc_density1(i={i}, a={a}), bln_count={bln_count}, bln_numba={bln_numba}")
    if i > len(aryprimes) and i <= 2**30:
        fill_primes(i + 2)
    if bln_count:
        if len(a) in hsh_count_all:
            hsh_count_all[len(a)] += 1
        else:
            hsh_count_all[len(a)] = 1
        is_prime = True
        for i in range(0, len(a)):
            if not aryprimes[a[i]]:
                is_prime = False
        if is_prime:
            if len(a) in hsh_count_prime:
                hsh_count_prime[len(a)] += 1
            else:
                hsh_count_prime[len(a)] = 1
    tcalc = time.time()
    if bln_numba:
        frac1 = calc_density_numba(i, a, max_sum)
    else:
        frac1 = calc_density_python(i, a, max_sum)
    total_calc_density += (time.time() - tcalc)
    return frac1


spec = [
    ('size', numba.int64),
    ('keys_capacity', numba.int64),
    ('values_capacity', numba.int64),
    ('keys_index', numba.int64),
    ('values_index', numba.int64),
    ('resizeable', numba.bool_),
    ('keys', numba.int64[:]),
    ('values', numba.int64[:]),
]

@numba.experimental.jitclass(spec)
class ArrayArray:
    def __init__(self, capacity, resizeable):
        self.size = 0
        self.keys_capacity = capacity
        self.values_capacity = 2*capacity
        self.keys_index = 0
        self.values_index = 0
        self.resizeable = resizeable
        self.keys = numpy.zeros(self.keys_capacity, dtype=numpy.int64)
        self.values = numpy.zeros(self.values_capacity, dtype=numpy.int64)
    
    def append(self, ary):
        if self.resizeable and self.values_index + len(ary) >= self.values_capacity:
            self.values_capacity += 2048
            temp = numpy.zeros(self.values_capacity, dtype=numpy.int64)
            temp[:self.values_index] = self.values[:self.values_index]
            self.values = temp
        i = self.values_index
        for a in ary:
            self.values[self.values_index] = a
            self.values_index += 1
        j = self.values_index - 1
        if self.resizeable and self.keys_index + len(ary) >= self.keys_capacity:
            self.keys_capacity += 2048
            temp = numpy.zeros(self.keys_capacity, dtype=numpy.int64)
            temp[:self.keys_index] = self.keys[:self.keys_index]
            self.keys = temp
        self.keys[self.keys_index] = i
        self.keys[self.keys_index + 1] = j
        self.keys_index += 2
    
    def removeAt(self, idx):
        self.keys[2*idx] = -1
        self.keys[2*idx + 1] = -1
    
    def __len__(self):
        return self.keys_index//2
    
    def __getitem__(self, idx):
        ary = numba.typed.List.empty_list(item_type=numpy.int64)
        idx = 2*idx
        if idx < 0 or idx >= self.keys_index:
            return ary
        i = self.keys[idx]
        j = self.keys[idx + 1]
        if i == -1 or j == -1:
            return ary
        ary.append(self.values[i])
        i += 1
        while i <= j:
            ary.append(self.values[i])
            i += 1
        return ary
    
    def to_list(self):
        return self.to_array()
    
    def to_array(self):
        return [self.values[self.keys[idx]:self.keys[idx+1]+1] for idx in range(0, self.keys_index, 2) if self.keys[idx] >= 0 and self.keys[idx+1] >= 0]

def to_array(aa):
    return [aa.values[aa.keys[idx]:aa.keys[idx+1]+1] for idx in range(0, aa.keys_index, 2) if aa.keys[idx] >= 0 and aa.keys[idx+1] >= 0]



#div = Divisors(aryprimes)
div = d.Divisors.get_instance()
div.set_verbose(False)

#@numba.jit(nopython=True)
def backtrack_divisors(n, target, factors, combinations, div):
    global min_factors
    global max_factors
    if target == 1:
        if len(factors) >= min_factors + 1 and len(factors) <= max_factors + 1 and factors[1] != n:
            bappend = True
            for j in range(len(factors) - 1, 1, -1):
                for k in range(j - 1, 0, -1):
                    if factors[j] % factors[k] == 0:
                        bappend = False
                        break
                if not bappend:
                    break
            if bappend:
                combinations.append(sorted(factors[1:]))
        return
    #for i in sympy.divisors(target)[1:]:
    for i in div.divisors(target)[1:]:
        if len(factors) == 1 or (len(factors) <= max_factors and i > factors[-1]):
            factors.append(i)
            backtrack_divisors(n, target // i, factors, combinations, div)
            factors.pop() 

#s = set(tuple(t) for t in [[4, 18, 22, 27, 77], [4, 18, 22, 33, 63], [6, 8, 9, 21, 363], [6, 8, 21, 27, 121], [6, 8, 21, 3267], [6, 8, 27, 33, 77], [6, 8, 27, 2541], [6, 8, 63, 1089], [6, 8, 77, 891], [6, 8, 81, 847], [6, 8, 121, 567], [6, 8, 189, 363], [6, 8, 231, 297], [27, 36, 44, 77], [48, 63, 1089], [48, 77, 891], [48, 81, 847], [48, 121, 567], [48, 189, 363], [48, 231, 297]])            

"""
factors = [1,]
combinations = sequence.ArrayArray(1024, True)
backtrack_sympy_divisors(3293136, 3293136, factors, combinations)
sequence.backtrack_sympy_divisors(3293136, 3293136, factors, combinations)
"""
def backtrack_sympy_divisors(n, target, factors, combinations):
    global min_factors
    global max_factors
    if target == 1:
        if len(factors) >= min_factors + 1 and len(factors) <= max_factors + 1 and factors[1] != n:
            bappend = True
            for j in range(len(factors) - 1, 1, -1):
                for k in range(j - 1, 0, -1):
                    if factors[j] % factors[k] == 0:
                        bappend = False
                        break
                if not bappend:
                    break
            if bappend:
                #if tuple(sorted(factors[1:])) in s:
                #    print(f"backtrack_sympy_divisors({n}, {target}, {factors}, combinations)")
                combinations.append(sorted(factors[1:]))
        return
    for i in sympy.divisors(target)[1:]:
        if len(factors) == 1 or (len(factors) <= max_factors and i > factors[-1]):
            factors.append(i)
            backtrack_sympy_divisors(n, target // i, factors, combinations)
            factors.pop() 


bln_backtrack_init = False
hsh_arrayarray = {}


"""
import sys
import os
import threading
import platformdirs
import pathlib
import importlib
sys.path.append('C:\\Users\\alex.weslowski\\Documents\\Python\\Sequence\\github')
import sequence_th as seq
import divisors as div
import time
# hshfractions = [-3550055125485641917]
hshfractions = [hash(frac) for frac in seq.setfractions]

bverbose = False
seq.min_factors = 2
seq.max_factors = 10
seq.max_denominator = 3
seq.bfile = True
seq.bdata = False
seq.verbose = bverbose
div.set_verbose(bverbose)
seq.filename = "sequence 1,2 1,3.txt"
seq.filename = "sequence 1_2.txt"
seq.directory = seq.directory_path()


i = 12
i = 65536
[fact for fact in seq.factorizations_outer(i, bln_remove_gt_half=False)]

i = 17149440
fact2 = []
for f1 in seq.factorizations_outer(i, bln_remove_gt_half=False):
    print(f"f1 = {f1}")
    frac1 = seq.calc_density1(i, f1)
    print(f"frac1 = {frac1}")
    if frac1.denominator <= seq.max_denominator:
        fact2.append((frac1.denominator, frac1, i, [int(x) for x in f1]))


frac1 = seq.calc_density1(17149440, [5, 6, 7, 11, 29, 256])
frac1 in seq.setfractions
hash(frac1) in [hash(frac) for frac in seq.setfractions]

print(seq.bln_count)
print(seq.bln_numba)
a = [3, 7, 816640]
frac1 = seq.calc_density1(17149440, a)
frac1 = seq.calc_density1(39443712, [3, 7, 11, 46, 58, 64])

bbreak = False
for i in range(0, 20):
    for j in [17149440, 39443712, 39621120]:
        fact2 = []
        for f1 in seq.factorizations_outer(j, bln_remove_gt_half=False):
            try:
                frac1 = seq.calc_density1(j, f1)
                if frac1.denominator == 2: print(f"f1 = {f1}, frac1 = {frac1}")
                if hash(frac1) in hshfractions:
                    fact2.append((frac1.denominator, frac1, j, [int(x) for x in f1]))
            except Exception as ex:
                pass
        print(fact2)
        if len(fact2) == 0:
            bbreak = True
            break
    if bbreak:
        break

f1 = [3, 5, 11, 103936]
frac1 = seq.Fraction(27773, 53592)

seq.q_in.put((2, 8388608))
seq.q_in.put((2, 16384))
seq.q_in.put((16777216, ))
loop = threading.Thread(target=seq.all_factors_loop)
seq.t0 = time.time()
loop.start()
seq.q_in.put(None)
writer = threading.Thread(target=seq.writer)
writer.start()
loop.join()
writer.join()

seq.min_factors = 2
seq.max_factors = 10
seq.bfile = True
seq.bdata = False
seq.verbose = True
seq.filename = "sequence 1_2.txt"
seq.directory = seq.directory_path()
seq.q_in.put((13440, 14882))
seq.q_in.put((549120, 591362))
seq.q_in.put((39443712, 39443712 + 2))
seq.q_in.put((39621120, 39621120 + 2))
loop = threading.Thread(target=seq.factors_loop, args=(seq.q_in, seq.q_out, False))
seq.t0 = time.time()
loop.start()
seq.q_in.put(None)
writer = threading.Thread(target=seq.writer)
writer.start()
loop.join()
writer.join()

seq.verbose = False
seq.q_in.put((2, 32768))
loop = threading.Thread(target=seq.factors_loop, args=(False,))
seq.t0 = time.time()
loop.start()
seq.q_in.put(None)
writer = threading.Thread(target=seq.writer)
writer.start()
loop.join()
writer.join()

"""

#factors = [1,]
#combinations = ArrayArray(2048, True)
#sequence.backtrack_divisors(3293136, 3293136, factors, combinations)
#combinations = sequence.ArrayArray(1024, True)
#combinations.append([2, 3])
#sequence.factorCombinations(3293136).to_array()
def factorCombinations(n2):
    global verbose
    global bln_cpp
    global bln_backtrack_init
    global total_factor_combinations
    global div
    if verbose: print(f"factorCombinations({n2})")
    tfactor = time.time()
    n = n2
    if not bln_cpp and not bln_backtrack_init:
        factors = [1,]
        combinations = ArrayArray(2, True)
        if bln_divisors:
            backtrack_divisors(1, 1, factors, combinations, div)
        else:
            backtrack_numba(1, 1, factors, combinations, small_factor_cache, factor_cache)
        bln_backtrack_init = True
    #factors = numba.typed.List.empty_list(item_type=numpy.int64)
    #combinations = []
    factors = [1,]
    combinations = ArrayArray(2048, True)
    if bln_cpp:
        combinations = d.Combinations(n)
        combinations.backtrack(n2, [])
        #combinations = combinations.get_arrayarray()
    elif bln_numba:
        backtrack_numba(n, n2, factors, combinations, small_factor_cache, factor_cache)
    elif bln_divisors:
        backtrack_divisors(n, n2, factors, combinations, div)
    total_factor_combinations += (time.time() - tfactor)
    if bln_count:
        key = (combinations.keys_capacity, combinations.values_capacity)
        if key in hsh_arrayarray:
            hsh_arrayarray[key] += 1
        else:
            hsh_arrayarray[key] = 1
    return combinations


#ary_tpl = sequence.factorCombinations(3293136)
#[ary_tpl[at] for at in range(0, len(ary_tpl))]
#sequence.to_array(sequence.factorizations_outer(3293136))
#frozenset([tuple(ary) for ary in sequence.factorizations_outer(3293136, bln_remove_gt_half=False).to_array()])
#sequence.factorizations_outer(3293136)
def factorizations_outer(n, bln_remove_gt_half=True):
    global min_factors
    global max_factors
    global verbose
    global total_factorizations_outer
    if verbose: print(f"factorizations_outer({n})")
    ary_tpl = factorCombinations(n)
    tfactorizations = time.time()
    at = -1
    while at < len(ary_tpl) - 1:
        at += 1
        if len(ary_tpl[at]) < min_factors or len(ary_tpl[at]) > max_factors:
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
    if verbose: print(f"factorizations_outer({n}) returning len(ary_tpl) = {len(ary_tpl)}")
    return ary_tpl


def factors_loop(q_in, q_out, bbreak):
    global verbose
    global aryprimes
    global istarted
    global bln_factors_loop
    global setfractions
    global max_sum
    hshfractions = [hash(frac) for frac in setfractions]
    max_sum = Fraction(1, 1)
    bstarted = False
    bln_factors_loop = True
    while bln_factors_loop:
        tpl = q_in.get()
        if tpl is None:
            q_out.put(None)
            break
        #if False and ((tpl[0] <= 39443712 and tpl[1] >= 39443712) or (tpl[0] <= 39621120 and tpl[1] >= 39621120)):
        #    verbose = True
        #else:
        #    verbose = False
        if verbose: print(f"factors_loop() tpl = {tpl}")
        if verbose: print(f"factors_loop() setfractions = {[str(x.numerator) + "/" + str(x.denominator) for x in list(setfractions)]}")
        if not bstarted:
            bstarted = True
            istarted += 1
        if tpl[1] > len(aryprimes) and tpl[1] <= 2**30:
            fill_primes(tpl[1] + 2)
        for i in range(tpl[0], tpl[1]):
            if aryprimes[i] or (i % 2 == 0 and aryprimes[i//2]) or (i % 3 == 0 and aryprimes[i//3]):
                continue
            #verbose = i in [39443712, 39621120]
            fact2 = []
            for f1 in factorizations_outer(i, bln_remove_gt_half=False):
                if verbose: print(f"factors_loop() i = {i}, f1 = {f1}")
                frac1 = calc_density1(i, f1)
                if verbose: 
                    print(f"factors_loop() i = {i}, frac1 = {frac1}, hash(frac1) = {hash(frac1)}, hshfractions = {hshfractions}")
                    print(f"factors_loop() denominator = {frac1.denominator}")
                    print(f"factors_loop() f1 = {[int(x) for x in f1]}")
                    print(f"factors_loop() ({hash(frac1)} in hshfractions) ? {hash(frac1) in hshfractions}")
                if hash(frac1) in hshfractions:
                    fact2.append((frac1.denominator, frac1, i, [int(x) for x in f1]))
                    if verbose: print(f"factors_loop() fact2[-1] = {fact2[-1]}")
                    if bbreak:
                        break
            if len(fact2) > 0:
                fact2 = sorted(fact2)
                q_out.put(fact2)
                if verbose:
                    for f2 in fact2:
                        print(f"factors_loop() {f2[1]}\t\t{f2[2]:,}\t\t{f2[3]}\t\t{len(f2[3])}")


def print_rows():
    global directory
    conn = sqlite3.connect(f"{directory}\\sequence.bin", check_same_thread=False)
    curs = conn.cursor()
    # _ = curs.execute("SELECT COUNT(*) FROM sequence")
    # curs.fetchone()
    _ = curs.execute("SELECT num, den, ord, ary, len FROM sequence WHERE ord >= 65520 ORDER BY ord")
    for row in curs.fetchall():
        print(row)
    conn.close()


"""
import sqlite3
conn = sqlite3.connect(f"{directory}\\sequence.bin", check_same_thread=False)
curs = conn.cursor()
_ = curs.execute("SELECT DISTINCT ord FROM sequence WHERE ord > (SELECT max(ord)-32 FROM sequence) LIMIT 32")
curs.fetchall()
_ = curs.execute("CREATE TABLE sequence (seq_id INTEGER PRIMARY KEY AUTOINCREMENT, num INTEGER, den INTEGER, ord INTEGER, len INTEGER)")
_ = curs.execute("CREATE TABLE array (ary_id INTEGER PRIMARY KEY AUTOINCREMENT, seq_id INTEGER, a INTEGER)")
_ = curs.execute("CREATE INDEX idx_sequence_ord ON sequence (ord)")
_ = curs.execute("CREATE INDEX idx_sequence_den_num ON sequence (den, num)")
_ = curs.execute("CREATE INDEX idx_sequence_len ON sequence (len)")
_ = curs.execute("CREATE INDEX idx_array_seq ON array (seq_id)")
conn.commit()
conn.close()
t0, i0, i1, i2
"""
def all_factors_loop(q_in, q_out):
    global verbose
    global max_denominator
    global aryprimes
    global istarted
    global bln_all_factors_loop
    bstarted = False
    bln_all_factors_loop = True
    while bln_all_factors_loop:
        tpl = q_in.get()
        if verbose: print(f"all_factors_loop() tpl = {tpl}")
        if not bstarted:
            bstarted = True
            istarted += 1
        if tpl is None:
            q_out.put(None)
            break
        if verbose:
            print("# ")
            print("# ")
            print(f"# all_factors_loop({tpl[0]}, {tpl[1]})")
            print("# ")
            print("# ")
        if tpl[1] > len(aryprimes) and tpl[1] <= 2**30:
            fill_primes(tpl[1] + 2)
        for i in range(tpl[0], tpl[1]):
            if aryprimes[i]:
                if i <= max_denominator:
                    q_out.put([(i, Fraction(1, i), i, [i,])])
                continue
            #fact1 = frozenset([tuple(ary) for ary in factorizations_outer(i, bln_remove_gt_half=False).to_array()])
            fact2 = []
            if verbose: print(f"all_factors_loop() i = {i}")
            for f1 in factorizations_outer(i, bln_remove_gt_half=False):
                if verbose: print(f"all_factors_loop() i = {i}, f1 = {f1}")
                frac1 = calc_density1(i, f1)
                if verbose: print(f"all_factors_loop() i = {i}, frac1 = {frac1}")
                if frac1.denominator <= max_denominator:
                    fact2.append((frac1.denominator, frac1, i, [int(x) for x in f1]))
            if len(fact2) > 0:
                fact2 = sorted(fact2)
                q_out.put(fact2)
                if verbose:
                    for f2 in fact2:
                        print(f"all_factors_loop() {f2[1]}\t\t{f2[2]:,}\t\t{f2[3]}\t\t{len(f2[3])}")
            if verbose: print(f"all_factors_loop() i = {i}, lineno = {sys._getframe(0).f_lineno}")
        if verbose: print(f"all_factors_loop() i = {i}, lineno = {sys._getframe(0).f_lineno}")


# sequence.ary_factors_loop([3293136,])
# [sequence.calc_density(3293136, ary) for ary in sequence.factorizations_outer(3293136, bln_remove_gt_half=False).to_array()]
def ary_factors_loop(ary):
    global aryprimes
    for i in ary:
        if aryprimes[i]:
            continue
        fact1 = frozenset([tuple(ary) for ary in factorizations_outer(i, bln_remove_gt_half=False).to_array()])
        fact2 = []
        for f1 in fact1:
            frac1 = calc_density1(i, f1)
            if frac1.numerator == 1 or frac1.denominator <= 32:
                fact2.append((frac1.denominator, frac1, i, list(f1)))
        for f2 in sorted(fact2):
            print(f"{f2[1]}\t\t{f2[2]:,}\t\t{f2[3]}\t\t{len(f2[3])}")


def check_factors(i, print_true, print_false):
    global setfractions
    max_sum = 1
    fact1 = frozenset([tuple(ary) for ary in factorizations_outer(i)])
    # (9, 12, 26, 235) in fact1
    blnfound = False
    for f1 in fact1:
        frac1 = calc_density1(i, f1, max_sum)
        if frac1 in setfractions:
            blnfound = True
            if print_true:
                print(f"{frac1} {i:,} {list(f1)}")
    if not blnfound and print_false:
        print(f"Not found! {i:,}")


hsh, minhshkeys, maxhshkeys = [], sys.maxsize, 0 # sys.maxsize = 2**63
bfile = True
bzip = False
bdata = False
directory = ""
filename = "sequence.txt"

def fill_hsh(i):
    global hsh
    global minhshkeys
    global maxhshkeys
    global lock
    global directory
    with lock:
        if not os.path.exists(f"{directory}\\sequence.bin"):
            return
        conn = sqlite3.connect(f"{directory}\\sequence.bin")
        curs = conn.cursor()
        # curs.execute("PRAGMA busy_timeout = 5000;")
        _ = curs.execute("CREATE INDEX IF NOT EXISTS idx_ord ON sequence (ord)")
        if len(hsh) == 0 or i < minhshkeys:
            print(f"fill_hsh() len(hsh) = {len(hsh)}, fact2[0][2] = {i}, minhshkeys = {minhshkeys}")
            # 10068080
            # 10174560
            _ = curs.execute("SELECT MAX(ord) FROM sequence")
            row = curs.fetchone()
            print(f"MAX(ord) = {row[0]}")
            maxhshkeys = row[0]
            _ = curs.execute("SELECT ord, COUNT(*) FROM sequence WHERE ord >= ? GROUP BY ord ORDER BY ord", (i,))
            for row in curs.fetchall():
                if minhshkeys == sys.maxsize:
                    minhshkeys = row[0]
                    hsh = [0,] * (maxhshkeys - minhshkeys + 1)
                if row[1] >= 100:
                    print(f"hsh[{row[0]}] = {row[1]}")
                hsh[row[0] - minhshkeys] = row[1]
            #minhshkeys = min(hsh.keys())
            #maxhshkeys = max(hsh.keys())
        _ = curs.execute("DROP INDEX IF EXISTS idx_ord")
        _ = curs.execute("DROP INDEX IF EXISTS idx_den_num")
        _ = curs.execute("DROP INDEX IF EXISTS idx_len")
        conn.execute("VACUUM")
        conn.commit()
        conn.close()


factscache = 72
linescache = 144
writescache = 2
#filebuffer = 32768
filebuffer = 8192
icompleted = 0

def writer(q_out):
    global verbose
    global inumthreads
    global icompleted
    global lock
    global t0
    global hsh
    global minhshkeys
    global maxhshkeys
    global directory
    global filename
    global factscache
    global linescache
    global writescache
    global filebuffer
    
    global bfile
    global bzip
    global bdata
    global total_file
    global total_data
    
    global total_factor_combinations
    global total_factorizations_outer
    global total_calc_density
    global total_writer
    
    global bln_keyboard_interrupt
    global bln_writer
    bln_writer = True
    
    # fact2 = q_out.get(block=False)
    # if bdata:
    #     fill_hsh(fact2[0][2])
    
    bfirst = True
    bfileclosed = False
    bdataclosed = False
    conn, curs, facts, lines, data = None, None, [], [], []
    f_zip, f_buf, f_txt = None, None, None
    try:
        if bdata:
            conn = sqlite3.connect(f"{directory}\\sequence.bin")
            curs = conn.cursor()
            curs.execute("PRAGMA journal_mode = MEMORY;")
            curs.execute("PRAGMA temp_store = MEMORY;")
            # curs.execute("PRAGMA synchronous = OFF;")
            curs.execute("PRAGMA cache_size = 262144;")
            curs.execute("PRAGMA page_size = 16384;")
            conn.commit()
            curs.execute("BEGIN TRANSACTION;")
        if bfile:
            if bzip:
                f_zip = gzip.open(f"{directory}\\{filename}.gz", mode="ab", compresslevel=7, encoding="ascii")
                f_buf = io.BufferedWriter(f_zip, buffer_size=filebuffer)
                f_txt = io.TextIOWrapper(f_buf, encoding='ascii')
            else:
                f_txt = open(f"{directory}\\{filename}", "a", buffering=filebuffer)
        
        i0, i1, itotal, ifacts, ilines, iwrites, icompleted = 0, 0, 0, 0, 0, 0, 0
        if verbose:
            print(f"writer() bfile = {bfile}")
            print(f"writer() bzip = {bzip}")
            print(f"writer() bdata = {bdata}")
            print(f"writer() directory = {directory}, filename = {filename}")
            print(f"writer() inumthreads = {inumthreads}, icompleted = {icompleted}")
        while bln_writer:
            fact2 = q_out.get(block=True)
            twriter = time.time()
            if bfirst:
                bfirst = False                
                if verbose: 
                    if fact2:
                        print(f"writer() bfile = {bfile}, bdata = {bdata}, len(fact2) = {len(fact2)}, fact2[0][2] = {fact2[0][2]}, icompleted = {icompleted}")
                    else:
                        print(f"writer() bfile = {bfile}, bdata = {bdata}, fact2 = None, icompleted = {icompleted}")
            if fact2 is None:
                icompleted += 1
                if icompleted == inumthreads:
                    print(f"writer() icompleted = {icompleted}, inumthreads = {inumthreads}")
                    dt = (time.time() - t0)/60
                    total_writer += (time.time() - twriter)
                    print(f"{round(dt, 2)} minutes ~ {round((i1 - i0)/dt, 1)} per min")
                    break
                else:
                    if verbose: print(f"writer() fact2 is None")
                    continue
            if i0 == 0:
                #print(f"i0 = {i0}, fact2 = {fact2}")
                i0 = fact2[0][2]
            else:
                #print(f"i0 = {i0}, fact2 = {fact2}")
                i1 = fact2[0][2]
            if bdata:
                if fact2[0][2] <= maxhshkeys and fact2[0][2] >= minhshkeys and hsh[fact2[0][2] - minhshkeys] > 0:
                    print(f"writer() {hsh[fact2[0][2] - minhshkeys]} row{'s' if hsh[fact2[0][2] - minhshkeys] > 1 else ''} found for ord = {fact2[0][2]:,}")
                    continue
            itotal += len(fact2)
            ilines += len(fact2)
            ifacts += len(fact2)
            facts.extend(fact2)
            if verbose: print(f"writer() ilines = {ilines}")
            if ifacts >= factscache:
                sfacts = sorted(facts, key=lambda f2: f2[2])
                for f2 in sfacts[:factscache//2]:
                    print(f"{f2[1]}\t\t{f2[2]:,}\t\t{f2[3]}\t\t{len(f2[3])}")
                    if bfile:
                        lines.append(f"{f2[1]}\t{f2[2]}\t{f2[3]}\t{len(f2[3])}\n")
                    if bdata:
                        # data.append((f2[1].numerator, f2[1].denominator, f2[2], str(f2[3]), len(f2[3])))
                        _ = curs.execute("INSERT INTO sequence (num, den, ord, len) VALUES (?, ?, ?, ?);", (f2[1].numerator, f2[1].denominator, f2[2], len(f2[3])))
                        seq_id = curs.lastrowid
                        _ = curs.executemany("INSERT INTO array (seq_id, a) VALUES (?, ?);", [(seq_id, x) for x in f2[3]])                    
                ifacts = 0
                facts = sfacts[factscache//2:]
            if ilines >= linescache:
                iwrites += 1
                if verbose: print(f"ilines = {ilines}")
                if verbose: print(f"len(lines) = {len(lines)}")
                if verbose: print(f"iwrites = {iwrites}")
                with lock:
                    # 0.16 seconds writing to file
                    # 412.05 seconds writing to database
                    if bfile:
                        tfile = time.time()
                        _ = f_txt.writelines(lines)
                        if iwrites >= writescache:
                            f_txt.flush()
                        total_file += (time.time() - tfile)
                        #print(f"{round(time.time() - tfile, 2)} seconds writing to file")
                    if bdata:
                        tdata = time.time()
                        # f2 = (Fraction(1, 13), 64584, "[26, 36, 69]", 3)
                        # _ = curs.executemany("INSERT INTO sequence (num, den, ord, len) VALUES (?, ?, ?, ?);", data)
                        if iwrites >= writescache:
                            curs.execute("COMMIT;")
                            conn.commit()
                            curs.execute("BEGIN TRANSACTION;")
                        total_data += (time.time() - tdata)
                        print(f"{round(time.time() - tdata, 2)} seconds writing to database")
                if iwrites >= writescache:
                    iwrites = 0
                ilines = 0
                data = []
                lines = []
                dt = (time.time() - t0)/60
                total_writer += (time.time() - twriter)
                # 0.68 minutes writing to file
                # 0.35 minutes writing to database
                # 48.99 total minutes factorCombinations()
                # 38.98 total minutes factorizations_outer()
                # 129.62 total minutes calc_density()
                # 0.14 total minutes writing to file
                # 0.06 total minutes writing to database
                if verbose:
                    print(f"# {round(total_factor_combinations/60, 2)} total minutes factorCombinations()")
                    print(f"# {round(total_factorizations_outer/60, 2)} total minutes factorizations_outer()")
                    print(f"# {round(total_calc_density/60, 2)} total minutes calc_density()")
                    print(f"# {round(total_writer/60, 2)} total minutes writer()")
                    print(f"# {round(total_file, 2)} total seconds writing to file")
                    print(f"# {round(total_data, 2)} total seconds writing to database")
                    #print(f"# i0 = {i0}")
                    #print(f"# i1 = {i1}")
                    #print(f"# i1 - i0 = {i1 - i0}")
                    print(f"# itotal = {itotal} ~ {round(itotal/dt, 1):.1f} per min")
                    print(f"# {round(dt, 2):.2f} mins ({round(dt/60, 2):.2f} hrs) ~ {round((i1 - i0)/dt, 1):.1f} per min")
            else:
                total_writer += (time.time() - twriter)
            q_out.task_done()
        if icompleted == inumthreads:
            with lock:
                if bfile:
                    tfile = time.time()
                    if verbose:
                        print(f"line = {sys._getframe(0).f_lineno}, ifacts = {ifacts}")
                        print(f"line = {sys._getframe(0).f_lineno}, len(facts) = {len(facts)}")
                        print(f"line = {sys._getframe(0).f_lineno}, ilines = {ilines}")
                        print(f"line = {sys._getframe(0).f_lineno}, len(lines) = {len(lines)}")
                    if len(facts) > 0:
                        for f2 in sorted(facts, key=lambda x: x[2]):
                            print(f"{f2[1]}\t\t{f2[2]:,}\t\t{f2[3]}\t\t{len(f2[3])}")
                            s = f"{f2[1]}\t{f2[2]}\t{f2[3]}\t{len(f2[3])}\n"
                            if s not in lines:
                                lines.append(s)
                    if ilines > 0:
                        _ = f_txt.writelines(lines)
                        ilines = 0
                        lines = []
                        ifacts = 0
                        facts = []
                    f_txt.flush()
                    if not bzip:
                        f_txt.close()
                    else:
                        f_txt.detach()
                        f_zip.flush()
                        f_zip.close()
                    total_file += (time.time() - tfile)
                    bfileclosed = True
                if bdata:
                    if conn.in_transaction:
                        curs.execute("COMMIT;")
                    conn.commit()
                    conn.close()
                    bdataclosed = True
    except Exception as ex:
        #traceback.print_tb(ex.__traceback__)
        print(traceback.format_exc())
        pass
    finally:
        dt = (time.time() - t0)/60
        print(f"icompleted = {icompleted}")
        print(f"inumthreads = {inumthreads}")
        if verbose:
            print(f"bzip = {bzip}")
            print(f"bfile = {bfile}")
            print(f"bfileclosed = {bfileclosed}")
            print(f"line = {sys._getframe(0).f_lineno}, ifacts = {ifacts}")
            print(f"line = {sys._getframe(0).f_lineno}, len(facts) = {len(facts)}")
            print(f"line = {sys._getframe(0).f_lineno}, ilines = {ilines}")
            print(f"line = {sys._getframe(0).f_lineno}, len(lines) = {len(lines)}")
        if bln_keyboard_interrupt or icompleted == inumthreads:
            with lock:
                if bfile and not bfileclosed:
                    tfile = time.time()
                    if len(facts) > 0:
                        for f2 in sorted(facts, key=lambda x: x[2]):
                            print(f"{f2[1]}\t\t{f2[2]:,}\t\t{f2[3]}\t\t{len(f2[3])}")
                            s = f"{f2[1]}\t{f2[2]}\t{f2[3]}\t{len(f2[3])}\n"
                            if s not in lines:
                                lines.append(s)
                    if ilines > 0:
                        _ = f_txt.writelines(lines)
                    f_txt.flush()
                    if not bzip:
                        f_txt.close()
                    else:
                        f_txt.detach()
                        f_zip.flush()
                        f_zip.close()
                    total_file += (time.time() - tfile)
                if bdata and not bdataclosed:
                    tdata = time.time()
                    if conn.in_transaction:
                        curs.execute("COMMIT;")
                    conn.commit()
                    conn.close()
                    total_data += (time.time() - tdata)
            print(f"# {round(total_factor_combinations/60, 2)} total minutes factorCombinations()")
            print(f"# {round(total_factorizations_outer/60, 2)} total minutes factorizations_outer()")
            print(f"# {round(total_calc_density/60, 2)} total minutes calc_density()")
            print(f"# {round(total_writer/60, 2)} total minutes writer()")
            print(f"# {round(total_file, 2)} total seconds writing to file")
            print(f"# {round(total_data, 2)} total seconds writing to database")
            #print(f"# i0 = {i0}")
            #print(f"# i1 = {i1}")
            #print(f"# i1 - i0 = {i1 - i0}")
            print(f"# itotal = {itotal} ~ {round(itotal/dt, 1)} per min")
            print(f"# {round(dt, 2)} mins ({round(dt/60, 2)} hrs) ~ {round((i1 - i0)/dt, 1)} per min")


t0 = 0
total_factorizations_outer = 0.0
total_factor_combinations = 0.0
total_calc_density = 0.0
total_writer = 0.0
total_file = 0.0
total_data = 0.0
istarted = 0
inumthreads = 1
q_in = queue.Queue()
q_out = queue.Queue()
lock = threading.Lock()


"""
import os
from pathlib import Path

current_file_path_str = __file__
print(f"1. Path to the current file (__file__): {current_file_path_str}")

module_directory_os = os.path.abspath(os.path.dirname(__file__))
print(f"\n2. Directory of the module (using os): {module_directory_os}")

current_path_obj = Path(__file__)
module_directory_pathlib = current_path_obj.parent
module_directory_absolute = module_directory_pathlib.resolve()
print(f"\n3. Directory of the module (using pathlib.Path): {module_directory_pathlib}")
print(f"   Absolute directory path (using pathlib.Path.resolve()): {module_directory_absolute}")
print(f"   String representation: {str(module_directory_absolute)}")

"""
def directory_path():
    global bdata
    global bfile
    
    hsh_dir = {}
    hsh_dir[(1, 'current',   'Current Working Directory ...')] = os.getcwd()
    hsh_dir[(2, 'module',    'Python Module Directory .....')] = pathlib.Path(__file__).parent.resolve()
    hsh_dir[(3, 'home',      'Home Directory ..............')] = os.path.expanduser('~')
    hsh_dir[(4, 'data',      'Data Directory ..............')] = platformdirs.user_data_dir()
    hsh_dir[(5, 'documents', 'Documents Directory .........')] = platformdirs.user_documents_dir()
    
    print("Choose a directory to write file to:")
    for key, value in hsh_dir.items():
        print(f"[{key[0]}] {key[2]} {value}")
    print("[6] Custom Path")
    print("[7] Output To Console")
    choice = input("Enter your choice (1-7): ")
    dir_path = ""
    for key in hsh_dir.keys():
        if choice == str(key[0]):
            dir_path = hsh_dir[key]
    if dir_path == "":
        if choice == '6':
            dir_path_str = input("Enter the directory path: ")
            dir_path = pathlib.Path(dir_path_str)
        elif choice == '7':
            bdata = False
            bfile = False
        else:
            print("Invalid choice. Please run the script again.")
            sys.exit(1)
    
    if bdata or bfile:
        if not dir_path.exists() or not dir_path.is_dir():
            print(f"Error: The directory '{dir_path}' does not exist.")
            sys.exit(1)
        is_readable = os.access(dir_path, os.R_OK)
        is_writable = os.access(dir_path, os.W_OK)
        if not is_readable:
            print("Error: You do not have read permissions for this directory.")
        if not is_writable:
            print("Error: You do not have write permissions for this directory.")
        if not is_readable or not is_writable:
            sys.exit(1)
    
    print(f"Selected path '{dir_path}'")
    print("")
    return dir_path


bln_all_factors_loop = False
bln_writer = False
bln_keyboard_interrupt = False


# 
# main loop 
# 
#   1,048,576 #  4.54 mins (0.1 hrs) ~ 210,133 per min
#   8,388,608 # 48.03 mins (0.8 hrs) ~ 168,542 per min
# 268,380,000
# 
# python.exe "C:\Users\alex.weslowski\Documents\Python\Sequence\sequence_th.py" 4 [(1,2)] 2 65536
# python.exe "C:\Users\alex.weslowski\Documents\Python\Sequence\sequence_th.py" 1 [(1,2)] 2 1048576
# python.exe "C:\Users\alex.weslowski\Documents\Python\Sequence\sequence_th.py" 8 [(1,2)] 2 8388608
# python.exe "C:\Users\alex.weslowski\Documents\Python\Sequence\sequence_th.py" 2 2 39410944 39653888
# python.exe "C:\Users\alex.weslowski\Documents\Python\Sequence\sequence_th.py" 4 2 8388608 16777216
# python.exe "C:\Users\alex.weslowski\Documents\Python\Sequence\sequence_th.py" 4 2 2 268380000
# 
def main():
    global verbose
    global directory
    global filename
    global setfractions
    global q_in
    global q_out
    global t0
    global bln_numba
    global aryprimes
    global inumthreads
    global istarted
    global icompleted
    global bln_factors_loop
    global bln_all_factors_loop
    global bln_writer
    global bln_keyboard_interrupt
    
    print(sys.version)
    print("")
    args = sys.argv[1:]
    directory = directory_path()
    
    if args[0].lower() == "debug":
        # import sqlite3
        conn = sqlite3.connect(f"{directory}\\sequence.bin", check_same_thread=False)
        curs = conn.cursor()
        _ = curs.execute("SELECT DISTINCT ord FROM sequence WHERE ord > (SELECT max(ord)-32 FROM sequence) LIMIT 32")
        print(curs.fetchall())
        return 
    
    imult = 8192
    istarted = 0
    inumthreads = int(args[0])
    ary = eval(args[1])
    strary = str(ary)[1:-1].replace("),(", ") (").replace(", ", ",")
    setfractions = frozenset([Fraction(tpl[0], tpl[1]) for tpl in ary])
    filename = f"sequence {strary}.txt"
    i0, i1 = int(args[2]) - inumthreads * imult, int(args[3])
    if i1 > 2**16:
        fill_primes(i1 + 2)
    if i0 < 2:
        i0 = 2
    print(f"main() starting process with inumthreads={inumthreads}, setfractions={ary}, istart={i0}, ifinish={i1}")
    
    # inumthreads, i0, i1 = 2, 2, 32768
    # i, imult = i0, 8192
    # while i < i1:
    #   for t in range(0, inumthreads):
    #       print((i + t * imult, min(i1, i + (t + 1) * imult)))
    #   i += inumthreads * imult
    i, t0 = i0, time.time()
    
    if True:
        if i > 12:
            fill_hsh(i)
        
        for frac in setfractions:
            if i0 <= frac.denominator:
                q_out.put([(frac.denominator, Fraction(1, frac.denominator), frac.denominator, [frac.denominator,]),])
        
        th = [object(),] * inumthreads
        while i < i1:
            for t in range(0, inumthreads):
                q_in.put((i + t * imult, min(i1, i + (t + 1) * imult)))
            i += inumthreads * imult
        for t in range(0, inumthreads):
            # th[t] = threading.Thread(target=all_factors_loop, args=(q_in, q_out))
            # factors_loop(t0, i0, i1, i2, bbreak)
            th[t] = threading.Thread(target=factors_loop, args=(q_in, q_out, False))
            th[t].start()
        for t in range(0, inumthreads):
            q_in.put(None)
        print(f"main() istarted = {istarted}, inumthreads = {inumthreads}")
        while istarted < inumthreads:
            time.sleep(1)
            print(f"main() istarted = {istarted}, inumthreads = {inumthreads}")
        print("")
        
        writer_th = threading.Thread(target=writer, args=(q_out,))
        writer_th.start()
        try:
            while icompleted < inumthreads:
                time.sleep(2)
        except KeyboardInterrupt:
            bln_keyboard_interrupt = True
            bln_factors_loop = False
            bln_all_factors_loop = False
            bln_writer = False
        try:
            for t in range(0, inumthreads):
                th[t].join()
            writer_th.join()
        except KeyboardInterrupt:
            pass
    
    if False:
        while i < i1:
            i += inumthreads * imult
            pr = [object(),] * inumcores
            for p in range(0, inumthreads):
                pr[p] = Process(target=factors_loop, args=(q_in, q_out, False))
                #all_factors_loop(time.time(), 2, 2, 65536)
                #pr[p] = Process(target=all_factors_loop, args=(q_in, q_out))
                pr[p].start()
            writer_pr = Process(target=writer, args=(q_out,))
            writer_pr.start()
            for p in range(0, inumthreads):
                pr[p].join()
            writer_pr.join()
        

if __name__ == '__main__':
    main()
