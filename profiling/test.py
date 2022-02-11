"""A simple example to show how to maintain unit tests while doing optimization"""

import time


def test_some_fn():
    """check basic behaviors for our function"""
    assert some_fn(2) == 4
    assert some_fn(1) == 1
    assert some_fn(-1) == 1

# check for line_profiler or memory_profiler in the local scope
# both are injected by their respective tools or they're absent
# if these tools aren't be used (in which case we need to substitute a dummy @profile decorator)
# dir(object) returns a list of attributes or methods of given object
# dir() returns a list of names in current local scope
if 'line_profiler' not in dir() and 'profile' not in dir():
    def profile(func):
        return func


@profile
def some_fn(x):
    time.sleep(1)
    return x ** 2


if __name__ == "__main__":
    print(f"Example call `some_fn(2)` == {some_fn(2)}")