import mpd
import signal

class KillMe:

    def __init__(self):
        self.kill_me = False
        signal.signal(signal.SIGINT, self._kill_callback)
        signal.signal(signal.SIGTERM, self._kill_callback)

    def _kill_callback(self, signum, frame):
        self.logger.info(f"Service killed by {signum}")
        self.kill_me = True

def exec_mpc_func(mpc, func, *args):
    try:
        mpc.ping()
    except mpd.ConnectionError:
        mpc.connect("localhost", 6600)
    return func(*args)
