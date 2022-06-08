import multiprocessing
import utils

class Thread(object):
    """Initializes the general thread service

    Args:
        name (str): The name of the service for queuing and logging
        state (State): The shared state with other services
    """
    def __init__(self, name, state):
        self._lock = multiprocessing.Lock()
        self._active = False
        self._thread = multiprocessing.Process(target=self._monitor)
        self._thread.name = name
        self._thread.daemon = True
        self.state = state
        self.set_queue()

    def set_queue(self):
        """Set the queue variable if it is available
        """
        queue = self.state.get_queue(self._thread.name)
        if queue:
            self.queue = queue

    def start(self):
        """Start the actual thread
        """
        with self._lock:
            self._active = True
        utils.log('{} starting...'.format(self._thread.name))
        self._thread.start()

    def _monitor(self):
        """The thread function that will be running
        """
        pass

    def running(self):
        """Check with a lock if the thread should still be running or not

        Returns:
            bool: If the thread should still be running
        """
        with self._lock:
            return self._active

    def stop(self):
        """Terminate the thread and close all sub tasks. 
        """
        with self._lock:
            self._active = False
        self._thread.terminate()
        self._thread.join()
        utils.log('{} stopped.'.format(self._thread.name))
