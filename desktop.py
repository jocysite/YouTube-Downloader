"""
Desktop launcher for YouTube Downloader.

Runs the Flask backend on a local port in a background thread and renders the
existing web UI inside a native desktop window using pywebview. This lets the
project ship as a standalone, installable application (no browser, no server,
no account) while reusing the Flask app unchanged.
"""
import os
import socket
import sys
import threading
import time
from urllib.request import urlopen


def _ensure_safe_stdio():
    """Make stdout/stderr safe for a windowed build.

    In a PyInstaller windowed (no-console) build stdout/stderr can be ``None``,
    and when a console is attached it may use a legacy codepage that can't encode
    the emoji used in log messages. Both cases would crash the app, so route
    missing streams to devnull and force UTF-8 with replacement elsewhere."""
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if stream is None:
            setattr(sys, name, open(os.devnull, "w", encoding="utf-8"))
        else:
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


_ensure_safe_stdio()

import webview

from app import app, get_downloads_folder

HOST = "127.0.0.1"


def find_free_port():
    """Pick an available TCP port on the loopback interface."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, 0))
        return sock.getsockname()[1]


def run_server(port):
    """Run the Flask app. Reloader is disabled so it works in a thread/frozen build."""
    app.run(host=HOST, port=port, debug=False, use_reloader=False, threaded=True)


def wait_until_ready(url, timeout=15.0):
    """Block until the local server responds or the timeout elapses."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=1):
                return True
        except Exception:
            time.sleep(0.1)
    return False


class Api:
    """JavaScript-callable bridge exposed to the web UI."""

    def close_app(self):
        """Close every app window, which ends webview.start() and exits."""
        for win in list(webview.windows):
            win.destroy()


def main():
    port = find_free_port()
    url = f"http://{HOST}:{port}"

    server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    server_thread.start()

    wait_until_ready(url)

    print("=" * 50)
    print("🎥 YouTube Downloader (Desktop)")
    print("📁 Downloads will be saved to:", get_downloads_folder())
    print("=" * 50)

    webview.create_window(
        "YouTube Downloader",
        url,
        width=1100,
        height=820,
        min_size=(800, 600),
        js_api=Api(),
    )
    webview.start()


if __name__ == "__main__":
    main()
