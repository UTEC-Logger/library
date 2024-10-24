import inspect
from os.path import basename
from time import time, strftime, localtime


def get_time_now():
    current_time = time()

    s = int(current_time)
    ms = int((current_time - s) * 1000)

    formatted_time = strftime('%Y-%m-%d %H:%M:%S', localtime(s))

    return f"{formatted_time}.{ms:03d}"


def get_current_frame():
    return inspect.currentframe().f_back.f_back


def get_file_name(frame):
    return basename(frame.f_code.co_filename)


def get_line_number(frame):
    return frame.f_lineno
