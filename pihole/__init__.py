import threading
import utils
import time
class PiHole(object):

    def __init__(self, state):
        self._lock = threading.Lock()
        self._active = False

        self._thread = threading.Thread(target=self._pi_hole_monitor)
        self._thread.daemon = True

    def start(self):

        with self._lock:
            self._active = True
        utils.log('[Pi Hole] Starting.')
        self._thread.start()
    def _pi_hole_monitor(self):

        utils.restart_upon_crash(self._pi_hole_thread)

    def _pi_hole_thread(self):
        while True:
            print("hallo")
            time.sleep(2)
            with self._lock:
                if not self._active:
                    return
    def stop(self):
        with self._lock:
            self._active = False

        self._thread.join()

        utils.log('[Pi Hole] Stopped.')