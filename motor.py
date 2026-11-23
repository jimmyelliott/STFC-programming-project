import threading

class SimpleMotor:
    def __init__(self, clock=time.monotonic):
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        # ...position, velocity, clock...

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()            # wait for the thread to finish

    def _run(self):
        while not self._stop_event.wait(0.1):   # sleeps 0.1 s; returns True once stopped
            self.update()