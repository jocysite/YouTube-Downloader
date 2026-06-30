"""
Afriway Downloader — desktop entry point.
Starts Flask in a background thread, waits for it to be ready,
then opens a native pywebview window.
"""
import json
import os
import socket
import sys
import threading
import time


def _resource(rel):
    """Resolve a path relative to the bundle root (works both frozen and dev)."""
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, rel)


PORT = 5050

_DEFAULT_WIDTH  = 1000
_DEFAULT_HEIGHT = 700
_MIN_WIDTH      = 860
_MIN_HEIGHT     = 600


def _get_size_file():
    if getattr(sys, 'frozen', False):
        data_dir = os.path.join(
            os.environ.get('APPDATA', os.path.expanduser('~')), 'AfriWayDownloader')
    else:
        data_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(data_dir, 'window.json')


def _load_window_size():
    try:
        with open(_get_size_file(), 'r') as f:
            d = json.load(f)
        w = max(_MIN_WIDTH,  int(d.get('width',  _DEFAULT_WIDTH)))
        h = max(_MIN_HEIGHT, int(d.get('height', _DEFAULT_HEIGHT)))
        return w, h
    except Exception:
        return _DEFAULT_WIDTH, _DEFAULT_HEIGHT


def _save_window_size(w, h):
    try:
        path = _get_size_file()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump({'width': w, 'height': h}, f)
    except Exception:
        pass


def _wait_for_flask(port, timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            s = socket.create_connection(('127.0.0.1', port), timeout=0.5)
            s.close()
            return True
        except OSError:
            time.sleep(0.1)
    return False


def _start_flask():
    from app import app, _load_sessions, _ensure_qr_code
    _load_sessions()
    _ensure_qr_code()
    app.run(host='127.0.0.1', port=PORT, debug=False, use_reloader=False)


if __name__ == '__main__':
    # Start Flask server
    t = threading.Thread(target=_start_flask, daemon=True)
    t.start()

    if not _wait_for_flask(PORT):
        print("ERROR: Flask server did not start in time.", file=sys.stderr)
        sys.exit(1)

    import webview
    width, height = _load_window_size()
    window = webview.create_window(
        'Afriway Downloader',
        f'http://127.0.0.1:{PORT}',
        width=width,
        height=height,
        min_size=(_MIN_WIDTH, _MIN_HEIGHT),
    )

    def on_closing():
        try:
            _save_window_size(window.width, window.height)
        except Exception:
            pass

    window.events.closing += on_closing
    webview.start()
