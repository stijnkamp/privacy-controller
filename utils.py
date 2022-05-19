import datetime
import traceback
import sys
import multiprocessing
import json
import os
import re
import mmap
import contextlib
import math


def get_current_thread_name():
    return multiprocessing.current_process().name


def log(*args):

    log_str = '[%s] ' % datetime.datetime.today()
    log_str += '[%s] ' % get_current_thread_name()
    log_str += ' '.join([str(v) for v in args])

    print(log_str)


class _SafeRunError(object):
    """Used privately to denote error state in safe_run()."""

    def __init__(self):
        pass


def safe_run(func, args=[], kwargs={}):
    """Returns _SafeRunError() upon failure and logs stack trace."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            return e
        err_msg = '=' * 80 + '\n'
        err_msg += 'Time: %s\n' % datetime.datetime.today()
        err_msg += 'Function: %s %s %s\n' % (func, args, kwargs)
        err_msg += 'Exception: %s\n' % e
        err_msg += 'Thread: %s\n' % get_current_thread_name()
        err_msg += str(traceback.format_exc()) + '\n\n\n'
        with multiprocessing.Lock():
            sys.stderr.write(err_msg + '\n')
            log(err_msg)
        return _SafeRunError()


def is_ip4(address):
    match = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", address)
    return bool(match) is True


def get_path(file):
    __location__ = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))
    return os.path.join(__location__, file)


def get_json(file):
    path = get_path(file)
    if os.path.isfile(path):
        f = open(get_path(file))
        return json.load(f)
    return None


def is_json(json_str):
    try:
        json.loads(json_str)
    except ValueError as e:
        return False
    return True


def search_in_file(filename, regex):
    regex = re.compile(regex.encode())
    offset = max(0, os.stat(filename).st_size - 15000)
    ag = mmap.ALLOCATIONGRANULARITY
    offset = ag * (int(math.ceil(offset/ag)))
    with open(filename, 'r') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_COPY, offset=offset)
        with contextlib.closing(mm) as txt:
            match = regex.search(txt)
            if match:
                return match.group().decode('UTF-8')
    return False
