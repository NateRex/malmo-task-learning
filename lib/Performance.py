# ==============================================================================================
# This file contains static functionality for timing the latency of functions, as well as
# evaluating the performance of statistical data relating to agent and human runs.
# ==============================================================================================
import timeit

class Timer:
    """
    Static class containing a collection of functions for timing the running time of certain methods and lambda expressions.
    """

    @staticmethod
    def __wrapFunction__(func, *args, **kargs):
        """
        Given a function and a list of arguments, return the function with those arguments as a
        callable object.
        """
        def __wrapped__():
            return func(*args, **kargs)
        return __wrapped__

    @staticmethod
    def timeFunctionCall(func, *args, **kargs):
        """
        Time how long it takes for a function to run, supplying the function name and a list of arguments.
        Returns the amount of time taken, in nanoseconds, as a float.
        """
        wrappedFunction = Timer.__wrapFunction__(func, *args, **kargs)
        timeTaken = timeit.timeit(wrappedFunction, number=1)
        return timeTaken * 1000000000