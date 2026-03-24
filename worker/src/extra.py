import inspect


class CMD:
    def __init__(self):
        self.content = ""

    def append(self, text: str = "", newline=True):
        self.content += text + "\n"*newline

    def reduce_right(self, n: int):
        self.content = self.content[:-n]

    def get(self) -> str:
        return self.content


def force_cursor(f):
    arg_name = "cur"

    def wrapper(*args, **kwargs):
        sig = inspect.signature(f)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        if arg_name in bound.arguments:
            return f(*args, **kwargs)

        con = args[0].con
        with con.cursor() as cur:
            try:
                kwargs[arg_name] = cur
                result = f(*args, **kwargs)
                con.commit()
                return result
            except Exception as e:
                con.rollback()
                raise e

    return wrapper


def fetch_adjust(return_single=False):
    def decorator(f):
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            if return_single:
                if len(result) == 0:
                    return None
                return result[0][0]
            if len(result[0]) == 1:
                return [data for data, in result]
            return result
        return wrapper
    return decorator
