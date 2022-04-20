import datetime
import traceback
import sys
import threading
import time

_lock = threading.Lock()

def log(*args):

    log_str = '[%s] ' % datetime.datetime.today()
    log_str += ' '.join([str(v) for v in args])

    print(log_str)

class _SafeRunError(object):
    """Used privately to denote error state in safe_run()."""
    def __init__(self):
        pass
def restart_upon_crash(func, args=[], kwargs={}):
    """Restarts func upon unexpected exception and logs stack trace."""
    while True:
        result = safe_run(func, args, kwargs)
        if isinstance(result, _SafeRunError):
            time.sleep(1)
            continue
        return result
def safe_run(func, args=[], kwargs={}):
    """Returns _SafeRunError() upon failure and logs stack trace."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        err_msg = '=' * 80 + '\n'
        err_msg += 'Time: %s\n' % datetime.datetime.today()
        err_msg += 'Function: %s %s %s\n' % (func, args, kwargs)
        err_msg += 'Exception: %s\n' % e
        err_msg += str(traceback.format_exc()) + '\n\n\n'
        with _lock:
            sys.stderr.write(err_msg + '\n')
            log(err_msg)
        return _SafeRunError()
