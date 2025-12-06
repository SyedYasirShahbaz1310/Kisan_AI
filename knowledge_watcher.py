import os
import time
import threading
from typing import Callable


class KnowledgeWatcher:
    def __init__(self, docs_dir: str, callback: Callable[[], None], poll_interval: float = 5.0):
        self.docs_dir = docs_dir
        self.callback = callback
        self.poll_interval = poll_interval
        self._stop = threading.Event()
        self._mtimes = {}

    def _scan(self):
        mtimes = {}
        if not os.path.exists(self.docs_dir):
            return mtimes
        for root, _, files in os.walk(self.docs_dir):
            for f in files:
                path = os.path.join(root, f)
                try:
                    mt = os.path.getmtime(path)
                    mtimes[path] = mt
                except Exception:
                    continue
        return mtimes

    def start(self):
        # initialize
        self._mtimes = self._scan()

        def _run():
            while not self._stop.is_set():
                time.sleep(self.poll_interval)
                new = self._scan()
                if new != self._mtimes:
                    self._mtimes = new
                    try:
                        self.callback()
                    except Exception:
                        pass

        t = threading.Thread(target=_run, daemon=True)
        t.start()

    def stop(self):
        self._stop.set()
