"""Examples of basic data structures used in python: list, tuple, dict, set, iterators and generators"""
from itertools import takewhile


def find_power2_no_less(n):
    return 1 << int(n-1).bit_length()


def get_mask(num_elem=1):
    """how to find mask (minimal memory blocks to allocate) given the number of elements"""
    num_bkts = num_elem * (2 / 3 + 1)   # num_bkt * 0.6 >= num_elem
    return bin(find_power2_no_less(num_bkts)-1)


def index_seq(key, mask=0b111, PERTURB_SHIFT=5):
    """probing logic used by CPython 3.7 dictionary lookup sequence"""
    perturb = hash(key)
    i = perturb & mask  # make sure index in range
    yield i
    while True:
        perturb >>= PERTURB_SHIFT
        i = (i * 5 + perturb + 1) & mask
        yield i


def check_index_seq(key, mask=0b111, n=8):
    """produce a sequence of n lookup indices given a key and mask"""
    res = []
    gen = index_seq(key, mask=mask)
    for i in range(n):
        res.append(next(gen))
    return res


def dict_resize_seq(n=1):
    """produce a sequence of actual dict sizes after n resizings, resize only happens on insert"""
    space = 8
    for i in range(n):
        yield space
        space = (int(space * 2 / 3) + 1) * 3


# hashable objects must implement __hash__ and __eq__, the defaults are using memory placement id
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# use list vs. generator
def fib_list(num_items):
    numbers = []
    a, b = 0, 1
    while len(numbers) < num_items:
        numbers.append(a)
        a, b = b, a + b
    return numbers


def fib_gen(num_items):
    a, b = 0, 1
    while num_items:
        yield a
        a, b = b, a + b
        num_items -= 1


# list comprehension consumes more memory
# divisible_by_three = len([n for n in fib_list(1000) if n % 3 == 0])
# generator comprehension not much memory
# divisible_by_three = sum(1 for i in fib_gen(1000) if i % 3 == 0)

def fib():
    """infinite generator for a fibonaci sequence"""
    i, j = 0, 1
    while True:
        yield j
        i, j = j, i + j


# how many Fibonacci numbers below 5000 are odd?
def fib_naive():
    i, j = 0, 1
    count = 0
    while j <= 5000:
        if j % 2 == 1:
            count += 1
        i, j = j, i + j
    return count


def fib_transform():
    count = 0
    for f in fib():
        if f > 5000:
            break
        if f % 2:
            count += 1
    return count


def fib_succinct():
    first_5000 = takewhile(lambda x: x <= 5000, fib())
    return sum(1 for x in first_5000 if x % 2)



