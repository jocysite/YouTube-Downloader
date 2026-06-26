# Afriway Downloader

A multi-type download manager built with Python and Flask, inspired by the spirit of Africa. Download YouTube videos and playlists, torrent files, direct files, and videos from 1 000+ sites — all from one clean, dark-themed web interface.

---

## Features

| Tab | What you can download |
|---|---|
| **YouTube** | Videos & playlists — pick exact video/audio quality, download as MP4 or MP3 |
| **Torrent** | Magnet links, `.torrent` URLs, or upload a `.torrent` file directly |
| **Others** | Direct files (`.exe`, `.zip`, images…) and videos from 1 000+ sites via yt-dlp |
| **All Downloads** | Unified queue with live search, type/status filters, real-time progress |

**More highlights:**

- Real-time progress bars and status polling (every 2 seconds)
- Persistent download history — survives page refresh without restarting downloads
- **"Show in folder"** button opens the file location in Explorer after completion
- Missing file detection — if a completed file was moved, shows a clear warning
- Custom download location via native OS folder picker
- Fully responsive — works on desktop and mobile browsers
- African-inspired dark UI with gold, green, and blue brand colours

---

## Requirements

### Python

```
Python >= 3.10
```

Install all Python dependencies:

```bash
pip install -r requirements.txt
```

### System tools

These are **not** Python packages — install them once on your machine:

#### FFmpeg (required for YouTube video+audio merging)

| OS | Command |
|---|---|
| Windows | `winget install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html) |
| macOS | `brew install ffmpeg` |
| Linux | `sudo apt install ffmpeg` |

> Without FFmpeg, YouTube downloads fall back to a single-stream format (no merging).

#### aria2c (required for torrent downloads)

| OS | Command |
|---|---|
| Windows | `winget install aria2` or download `aria2c.exe` from [GitHub Releases](https://github.com/aria2/aria2/releases) and place it next to `app.py` |
| macOS | `brew install aria2` |
| Linux | `sudo apt install aria2` |

> Torrent downloads are disabled if aria2c is not found. All other tabs work without it.

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/jocysite/Afriway-Downloader.git
cd Afriway-Downloader

# 2. (Recommended) Create a virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Open **http://localhost:5000** in your browser.

---

## How to Use

### YouTube Tab

1. Paste a YouTube video or playlist URL in the input field.
2. Click **Fetch URL** — loads the title and available formats.
3. Choose **Video + Audio** (MP4) or **Audio Only** (MP3).
4. Select your preferred video and audio quality.
5. For playlists, check/uncheck individual videos to skip them.
6. Click **Download Now** — progress appears in the queue below.

### Torrent Tab

1. **Paste a magnet link or `.torrent` URL** in the input, then click **Start Download**.
   — OR —
2. **Upload a `.torrent` file** using the file picker.

> Requires aria2c (see Requirements above).

### Others Tab

1. Paste any URL — a direct file link, a Vimeo/Twitter/Dailymotion video, or any yt-dlp-supported site.
2. Click **Analyze URL** — detects file type and shows name/size.
3. Click **Download** to start.

### Changing the Download Location

The **Save to:** bar at the top shows the current folder.

- Type a path and click **Apply**.
- Or click **Browse** to pick a folder with the native OS dialog.

Files are organised automatically:
- YouTube → `<download folder>/YouTube Downloads/`
- Everything else → `<download folder>/`

### All Downloads Tab

Shows every download (past and active) in one place.

- **Search bar** — filter by name or URL.
- **Type / Status dropdowns** — narrow the list.
- **"Show in folder"** button — opens the file location in Explorer after completion.
- **"File moved?"** button — appears when a completed file is no longer at its saved path.

---

## Project Structure

```
Afriway-Downloader/
├── app.py              # Flask backend — routes, download threads, session management
├── requirements.txt    # Python dependencies
├── downloads.json      # Auto-generated: persisted download history (git-ignored)
├── static/
│   ├── script.js       # Frontend — tabs, queue polling, all download flows
│   ├── style.css       # Responsive dark theme with brand colours
│   ├── AfriwayLogo.webp
│   └── qr-coffee.webp  # Auto-generated at startup
└── templates/
    └── index.html      # Single-page app shell
```

---

## Desktop App (planned)

The project is designed to be packaged as a standalone `.exe` using **PyInstaller**:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed \
  --add-data "templates;templates" \
  --add-data "static;static" \
  app.py
```

User data (`downloads.json`, settings) will be stored in `%APPDATA%\AfriWayDownloader\` automatically when running as an exe.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "aria2c not found" on Torrent tab | Install aria2c (see Requirements) and restart. Or place `aria2c.exe` in the same folder as `app.py`. |
| YouTube video has no audio or low quality | Install FFmpeg — without it yt-dlp cannot merge separate video and audio streams. |
| "Browse" folder picker doesn't open | Ensure tkinter is available: run `python -m tkinter`. On Linux: `sudo apt install python3-tk`. |
| Port 5000 already in use | `set FLASK_PORT=5001 && python app.py` (Windows) or `FLASK_PORT=5001 python app.py` (macOS/Linux). |

---

## Credits

Developed by **Yosef Mulatu**

If this app saves you time, [buy me a coffee](https://buymeacoffee.com/yosefmulatu) ☕

---

## License

MIT — free to use, modify, and distribute.
