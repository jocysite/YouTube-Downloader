# Afriway Downloader

> A multi-type download manager built with Python and Flask, inspired by the spirit of Africa. Download YouTube videos and playlists, torrents, direct files, and videos from 1 000+ sites — all from one clean, themed desktop interface.

<p align="center">
  <img src="static/AfriwayLogo.webp" width="120" alt="Afriway Logo" />
</p>

---

## Features

### Download Modes

| Tab | What you can download |
|---|---|
| **YouTube** | Videos & playlists — pick exact video and audio quality, download as MP4 or MP3 |
| **Torrent** | Magnet links, `.torrent` URLs, or upload a `.torrent` file directly |
| **Others** | Direct files (`.exe`, `.zip`, images…) and videos from 1 000+ sites via yt-dlp |
| **All Downloads** | Unified queue with live search, type/status filters, and real-time progress |

### Queue Controls

- **Pause / Resume** — per-item and bulk (Select All → Pause All / Resume All)
- **Retry** — resumes from partial `.part` files; direct downloads use HTTP Range requests
- **Re-download** — appears when a completed file has been moved or deleted
- **Remove from list** — removes the entry without touching the file
- **Delete file** — removes the entry and permanently deletes the file from disk
- **Copy link** — copies the original source URL to the clipboard
- **Show in folder** — opens Explorer at the file location after completion

### Afriway Folder Organisation

Files are automatically sorted by type into an `Afriway` folder on whichever drive you select:

```
Afriway/
├── Videos/     YouTube videos, audio, and yt-dlp downloads
├── Images/     Direct image downloads (.jpg, .png, .gif, .webp…)
├── App/        Executables and packages (.apk, .exe, .msi, .dmg…)
├── Folder/     YouTube playlists (one sub-folder per playlist)
└── Other/      Everything else (.zip, .pdf, .torrent content…)
```

- **System drive (C:)** → `C:\Users\<You>\Downloads\Afriway`
- **Any other drive** → `X:\Afriway`

### UI & Usability

- **Theme switcher** — Default (Afro Black), Dark, and Light themes; persists across sessions and exe restarts via server-side `prefs.json`
- **URL paste button** — clipboard paste icon inside the URL field for one-click paste
- **Right-click context menu** — custom Cut / Copy / Paste menu on the URL input
- **Themed native dropdowns** — all `<select>` elements match the dark gold theme including the native popup list
- **SweetAlert2 notifications** — all alerts and toasts styled to match the theme, no browser-native popups
- **Persistent history** — download sessions survive page refresh and server restart
- **Responsive layout** — works on desktop and mobile browsers

### YouTube Cookies Support

YouTube may restrict some formats for unauthenticated requests. To work around this:

1. Install the **"Get cookies.txt LOCALLY"** browser extension
2. Visit [youtube.com](https://www.youtube.com) while logged in
3. Export `cookies.txt` using the extension
4. In the app, open **Settings → YouTube Cookies** and upload the file

The cookies file is stored at `%APPDATA%\AfriWayDownloader\youtube_cookies.txt` and used automatically for all YouTube requests.

---

## Requirements

### Python

```
Python >= 3.10
```

```bash
pip install -r requirements.txt
```

### FFmpeg (required for YouTube video+audio merging)

| OS | Command |
|---|---|
| Windows | `winget install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html) |
| macOS | `brew install ffmpeg` |
| Linux | `sudo apt install ffmpeg` |

> Without FFmpeg, YouTube downloads fall back to a single-stream format (no separate video+audio merge).

### aria2c (required for Torrent downloads)

| OS | Command |
|---|---|
| Windows | `winget install aria2` or place `aria2c.exe` anywhere inside the project folder |
| macOS | `brew install aria2` |
| Linux | `sudo apt install aria2` |

> The app searches the project folder recursively; placing the binary anywhere under the project directory works.
> Torrent downloads are disabled if aria2c is not found. All other tabs work without it.

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/jocysite/Afriway-Downloader.git
cd Afriway-Downloader

# 2. (Recommended) Create a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Open **http://localhost:5000** in your browser, or use the desktop app (see below).

---

## How to Use

### URL Bar

A single URL field sits at the top of the page, always visible. Paste any URL there — YouTube, magnet link, direct file, or video site URL — then switch to the appropriate tab.

- Click the **clipboard icon** on the right of the field to paste from clipboard instantly
- **Right-click** the field for a Cut / Copy / Paste context menu

### YouTube Tab

1. Paste a YouTube video or playlist URL in the URL bar.
2. Click **Fetch URL** — loads the title and all available formats.
3. Choose **Video + Audio** (MP4) or **Audio Only** (MP3).
4. Select video quality and audio quality from the lists.
5. For playlists, uncheck any videos you want to skip.
6. Click **Download Now** — progress appears in the queue.

> If you see "format not available" errors, upload a cookies file in Settings (see YouTube Cookies above).

### Torrent Tab

1. Paste a magnet link or `.torrent` URL in the URL bar.
2. Click **Start Download**.
   — OR —
3. Use the **Upload .torrent file** picker.

### Others Tab

1. Paste any direct file link or yt-dlp-supported URL (Vimeo, Twitter/X, Dailymotion, etc.).
2. Click **Analyze URL** — detects file type and shows name/size.
3. Click **Download** to start.

### Drive Selector

The **Drive** dropdown lets you pick which drive the `Afriway` folder lives on. The resolved path shows as a preview. Click **Apply** to confirm.

### All Downloads Tab

Shows every download (past and present) in one place.

- **Search bar** — filter by name or URL
- **Type / Status dropdowns** — narrow the list
- **Bulk toolbar** — Select All → Pause All / Resume All
- **Per-item actions** — Pause, Resume, Retry, Copy link, Show in folder, Remove, Delete file

### Theme

Click the **palette icon** in the header to switch between **Default**, **Dark**, and **Light** themes. The choice is saved and restored on the next launch.

---

## Project Structure

```
Afriway-Downloader/
├── app.py                  # Flask backend — routes, download threads, session management
├── main.py                 # pywebview entry point for desktop/exe mode
├── requirements.txt        # Python dependencies
├── afriway.spec            # PyInstaller spec for building the .exe
├── rthook_afriway.py       # Runtime hook patching paths inside the frozen exe
├── downloads.json          # Auto-generated: persisted download history (git-ignored)
├── prefs.json              # Auto-generated: user preferences — theme, settings (git-ignored)
├── static/
│   ├── script.js           # Frontend — tabs, queue polling, all download flows
│   ├── style.css           # Responsive themed UI with gold/green/dark brand colours
│   ├── AfriwayLogo.webp    # In-app header logo
│   ├── AfriwayLogo.png     # Source logo for ICO generation
│   ├── afriway.ico         # Favicon + exe desktop icon
│   └── aria2-*/            # Bundled aria2c binary (Windows)
└── templates/
    └── index.html          # Single-page app shell
```

---

## Building the Desktop App

The app runs as a native desktop window using **pywebview** (wraps the OS WebView).

### Prerequisites

```bash
pip install pyinstaller pywebview
```

### Build

```bash
pyinstaller afriway.spec
```

The output executable is at `dist/AfriWayDownloader.exe`.

- User data (`downloads.json`, `prefs.json`, `youtube_cookies.txt`) is stored in `%APPDATA%\AfriWayDownloader\`
- No Python installation required on the target machine
- The desktop icon uses `AfriwayLogo.png` packaged into a multi-size `.ico`

---

## Troubleshooting

| Problem | Fix |
|---|---|
| YouTube "Requested format is not available" | Upload a `cookies.txt` file in **Settings → YouTube Cookies** |
| "aria2c not found" on Torrent tab | Download `aria2c.exe` from [GitHub Releases](https://github.com/aria2/aria2/releases) and place it anywhere in the project folder |
| YouTube video has no audio or poor quality | Install FFmpeg — without it yt-dlp cannot merge separate video+audio streams |
| Port 5000 already in use | `set FLASK_PORT=5001 && python app.py` (Windows) or `FLASK_PORT=5001 python app.py` (macOS/Linux) |
| "Copy link" / Paste doesn't work | The Clipboard API requires a secure context — access the app via `http://localhost`, not a raw IP |
| File shows "File moved?" after completion | The file was moved or deleted after download. Click **↩ Re-download** to fetch it again |
| Paused download won't resume after restart | The app restarts from the last saved position using the original URL and folder |
| Theme resets on every launch | Make sure `prefs.json` is writable in the app directory (or `%APPDATA%\AfriWayDownloader\` in exe mode) |

---

## Credits

Developed by **Yosef Mulatu**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Yosef%20Mulatu-0A66C2?logo=linkedin)](https://www.linkedin.com/in/yosefmulatu/)
[![Telegram](https://img.shields.io/badge/Telegram-@jocyJ-2CA5E0?logo=telegram)](https://t.me/jocyJ)
[![Email](https://img.shields.io/badge/Email-josephmulatu1%40gmail.com-D4AF37)](mailto:josephmulatu1@gmail.com)

If this app saves you time, [buy me a coffee ☕](https://buymeacoffee.com/yosefmulatu)

---

## License

MIT — free to use, modify, and distribute.
