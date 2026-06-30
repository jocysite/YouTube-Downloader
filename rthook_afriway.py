# PyInstaller runtime hook — runs before ANY user code in the frozen exe.
# Patches sys.stdout/sys.stderr to a working devnull stream when they are
# None or broken (console=False windowed build). This prevents yt_dlp and
# werkzeug from crashing the process with AttributeError before any Python
# exception handler is in place.
import sys
import os

if getattr(sys, 'frozen', False):
    _devnull = None
    for _attr in ('stdout', 'stderr'):
        _needs = False
        _s = getattr(sys, _attr, None)
        if _s is None:
            _needs = True
        else:
            try:
                _s.write('')
                _s.flush()
            except Exception:
                _needs = True
        if _needs:
            try:
                if _devnull is None:
                    _devnull = open(os.devnull, 'w', encoding='utf-8', errors='replace')
                setattr(sys, _attr, _devnull)
            except Exception:
                pass
