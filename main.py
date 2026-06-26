"""
Afriway Downloader — desktop entry point.
Starts Flask in a background thread, waits for it to be ready,
then opens a native pywebview window.
"""
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
    # Import here so sys.path adjustments above take effect first
    from app import app
    app.run(host='127.0.0.1', port=PORT, debug=False, use_reloader=False)


if __name__ == '__main__':
    # Start Flask server
    t = threading.Thread(target=_start_flask, daemon=True)
    t.start()

    if not _wait_for_flask(PORT):
        print("ERROR: Flask server did not start in time.", file=sys.stderr)
        sys.exit(1)

    import webview
    webview.create_window(
        'Afriway Downloader',
        f'http://127.0.0.1:{PORT}',
        width=1280,
        height=820,
        min_size=(860, 600),
    )
    webview.start()
