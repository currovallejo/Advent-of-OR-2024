import time


def timed(function):
    def wrapper(*args, **kwargs):
        if args and hasattr(args[0], '__class__'):
            func_name = f"{args[0].__class__.__name__}.{function.__name__}"
        else:
            func_name = function.__name__
        start = time.time()
        value = function(*args, **kwargs)
        end = time.time()
        print(f"Function {func_name} took {end - start} seconds to run\n")
        return value

    return wrapper
