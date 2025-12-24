# mcp_server/core.py
import sys, io, builtins, logging

class _JSONStdoutGuard(io.TextIOBase):
    def __init__(self, real):
        self._real = real
        self._armed = True
    @property
    def buffer(self): return getattr(self._real, "buffer", None)
    def write(self, s):
        if not s: return 0
        if self._armed:
            stripped = s.lstrip()
            if not stripped: return 0
            self._armed = False
            return self._real.write(stripped)
        return self._real.write(s)
    def flush(self): return self._real.flush()

_sys_stdout_real = sys.stdout
sys.stdout = _JSONStdoutGuard(sys.stdout)

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s", stream=sys.stderr, force=True)

_builtin_print = builtins.print
def _print_to_stderr(*args, **kwargs):
    kwargs.setdefault("file", sys.stderr)
    return _builtin_print(*args, **kwargs)
builtins.print = _print_to_stderr
