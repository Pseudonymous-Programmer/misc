import time

class Memoize:
    def __init__(self,func):
        self.stored = {}
        self.func = func
    def __call__(self,*args):
        if(args not in self.stored.keys()):
            self.stored[args] = self.func(*args)
        return self.stored[args]

@Memoize
def fib(n):
    if(n < 2):
        return n
    else:
        return fib(n - 1) + fib(n - 2)

for i in range(100):
    print(fib(i))
