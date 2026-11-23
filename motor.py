import threading
import time

MIN_POSITION = 0.0
MAX_POSITION = 1000.0
UPDATE_INTERVAL = 0.1


class SimpleMotor:
    def __init__(self, clock=time.monotonic):
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._clock = clock
        self._position = 0.0
        self._velocity = 0.0
        self._last_time = clock()

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()            # wait for the thread to finish

    def _run(self):
        while not self._stop_event.wait(UPDATE_INTERVAL):  # True once stopped
            self.update()

    # --- simulation -----------------------------------------------------

    def update(self):
        with self._lock:
            self._advance()

    def _advance(self):
        """Move position forward to 'now'. Caller must hold the lock."""
        now = self._clock()
        elapsed = now - self._last_time
        self._last_time = now
        # final position = initial position + (velocity * time)
        new_position = self._position + self._velocity * elapsed

        # enforce limits: clamp and force the motor to stop, but only when
        # moving *into* the limit (so v=5 at position 0 still moves off it)
        if new_position <= MIN_POSITION and self._velocity <= 0:
            new_position = MIN_POSITION
            self._velocity = 0.0
        elif new_position >= MAX_POSITION and self._velocity >= 0:
            new_position = MAX_POSITION
            self._velocity = 0.0

        self._position = new_position

    # --- commands -------------------------------------------------------

    def get_position(self):
        with self._lock:
            return self._position

    def get_velocity(self):
        with self._lock:
            return self._velocity

    def set_velocity(self, velocity):
        with self._lock:
            self._advance()                    # account for motion at the old velocity first
            self._velocity = velocity + 0.0    # "+ 0.0" turns -0.0 into 0.0

    def stop_motion(self):
        self.set_velocity(0.0)
