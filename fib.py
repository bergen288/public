from xz_settings import get_arg_list, check_attrs
from xz_settings import get_cwd
from pathlib import Path
path = Path(__file__).parent
get_cwd(path)

def get_arg_list(*args, **kwargs):
    """[summary: get list of args and kwargs]

    Returns:
        [type: list]: [description, list of args and kwargs]
    """
    arg_lst = []
    if args:
        arg_lst.append(', '.join(repr(arg) for arg in args))
    if kwargs:
        pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
        arg_lst.append(', '.join(pairs))
    arg_str = ', '.join(arg_lst)
    return arg_str

# def calculateFibonacci(n):
#     memoize = [-1 for x in range(n+1)]
#     return calculateFibonacciRecur(memoize, n)

# def calculateFibonacciRecur(memoize, n):
#     if n < 0:
#         print(f'The input vaule {n} is negative.  Please input a positive integer!')
#     elif isinstance(n, int) is False:
#         print(f'The input vaule {n} is not integer.  Please input a positive integer!')
#     elif n < 2:
#         return n
#     if memoize[n] < 0:
#         memoize[n] = calculateFibonacciRecur(
#             memoize, n - 1) + calculateFibonacciRecur(memoize, n - 2)
#     return memoize[n]
class BenchMark:
    def __init__(self, func):
        import datetime
        self.func = func
        self.start_time = datetime.datetime.now()
        print('Start Time is: ', self.start_time)
    def __call__(self, *args, **kwargs):
        import datetime
        signature = get_arg_list(*args, **kwargs)
        self.func(*args, **kwargs)
        end_time = datetime.datetime.now()
        total_time = end_time - self.start_time
        print('End Time is: ', end_time)
        print(f"The Turnaround Time of {self.func.__name__}({signature}) is {total_time}")

class Pyinst_Prof:
    def __init__(self, func):
        import datetime
        self.func = func
        self.start_time = datetime.datetime.now()
        print('Start Time is: ', self.start_time)
    def __call__(self, *args, **kwargs):
        import datetime
        signature = get_arg_list(*args, **kwargs)
        from pyinstrument import Profiler
        with Profiler(interval=0.001, async_mode='disabled') as pr:
            self.func(*args, **kwargs)
        pr.print()
        end_time = datetime.datetime.now()
        total_time = end_time - self.start_time
        print('End Time is: ', end_time)
        print(f"The Turnaround Time of Pyinstrument Profiling for {self.func.__name__}({signature}) is {total_time}")

class cProf:
    def __init__(self, func):
    # def __init__(self, func, file):
        import datetime
        self.func = func
        # self.file = file
        self.start_time = datetime.datetime.now()
        print('Start Time is: ', self.start_time)
    def __call__(self, *args, **kwargs):
        import datetime
        signature = get_arg_list(*args, **kwargs)
        import cProfile, pstats
        with cProfile.Profile() as pr:
            self.func(*args, **kwargs)
        pr.print_stats()
        # pr.dump_stats(self.file)
        end_time = datetime.datetime.now()
        total_time = end_time - self.start_time
        print('End Time is: ', end_time)
        print(f"The Turnaround Time of cProfile for {self.func.__name__}({signature}) is {total_time}")
        return pr

class Line_Prof:
    def __init__(self, func):
        import datetime
        self.func = func
        self.start_time = datetime.datetime.now()
        print('Start Time is: ', self.start_time)
    # @profile
    def __call__(self, *args, **kwargs):
        import datetime
        signature = get_arg_list(*args, **kwargs)
        from line_profiler import LineProfiler
        # f = self.func
        # f = self.func(*args, **kwargs)
        profile = LineProfiler()
        # check_attrs(pr)
        profile.enable()
        self.func(*args, **kwargs)
        # pr = profile(self.func)
        # f = pr(*args, **kwargs)
        # print('f is: ', f)
        profile.print_stats()
        profile.disable()
        # pr.print_stats()
        end_time = datetime.datetime.now()
        total_time = end_time - self.start_time
        print('End Time is: ', end_time)
        print(f"The Turnaround Time of line_profiler for {self.func.__name__}({signature}) is {total_time}")
        # return pr


# @profile
@Line_Prof
def calculateFibonacci(n):
    if n < 0:
        print(f'The input value {n} is negative.  Please input a positive integer!')
    elif isinstance(n, int) is False:
        print(f'The input value {n} is not an integer.  Please input a positive integer!')
    elif n <= 2:
        return 1
    else:
        return calculateFibonacci(n - 1) + calculateFibonacci(n - 2)

# @BenchMark
# @Pyinst_Prof
# @cProf
def main(N):
    print(f'The {N}th Fibonacci number is:',  calculateFibonacci(N))

if __name__ == '__main__':
    N = 6
    main(N)
    print('end')
# time_func(main)
# time_func(calculateFibonacci,  N =10, n=10)
# for n in range(1, N):
#     print(n, ':', calculateFibonacci(n))
# import pprofile
# from auto_profiler import Profiler, tree
# prof = Profile()
# with Profiler(depth=4):
# import statprof

# statprof.start()
# try:
#     # my_questionable_function()
#     print(N, ':', calculateFibonacci(N))
# finally:
#     statprof.stop()
#     statprof.display()


class BenchMark:
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **kwargs):
        import datetime
        self.start_time = datetime.datetime.now()
        print('Start Time is: ', self.start_time)
        try:
            self.func(*args, **kwargs)
        finally:
            end_time = datetime.datetime.now()
            total_time = end_time - self.start_time
            print('End Time is: ', end_time)
            signature = get_arg_list(*args, **kwargs)
            print(f"The Turnaround Time of {self.func.__name__}({signature}) is {total_time}")


class cProf(BenchMark):
    def __call__(self, *args, **kwargs):
        import cProfile
        with cProfile.Profile() as pr:
            BenchMark.__call__(self, *args, **kwargs)
        pr.print_stats()
