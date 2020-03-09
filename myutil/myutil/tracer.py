import sys

class SetTrace(object):
    def __init__(self, func):
        self.func = func

    def __enter__(self):
        sys.settrace(self.func)
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        sys.settrace(None)

def monitor(frame, event, arg):
    if event == "line":
        print(frame.f_code)
        print("")
        # print(frame.f_globals)
        # print(frame.f_locals)
    return monitor

def example():
    def foo():
        x = 0
        while True:
            print('bar')
            x += 1

    with SetTrace(monitor):
        foo()
