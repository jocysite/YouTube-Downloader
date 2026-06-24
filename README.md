# Afriway Downloader 🦅🌍

**Proudly African • Boldly Modern**

A **desktop application** for downloading YouTube videos and playlists with customizable quality and format options. Built with **Electron** and **Flask**, featuring an Ethiopian and Pan-African inspired design.

> "Ubuntu — I am because we are." Download smarter together.

## Features

- 🖥️ **Desktop Application** — Runs as a standalone native window (no browser needed)
- 🎥 Download individual YouTube videos
- 📋 Download entire playlists with selective video picking
- 🎯 Choose from multiple video quality options (360p, 720p, 1080p, etc.)
- 🎵 Select preferred audio/video format combinations
- ⚡ Smart quality fallback — automatically finds the best available quality
- 📁 Saves to your Downloads folder
- 🌅 **African-Inspired Theme** — Colors from the Ethiopian and Pan-African palette
- 🌐 **Swahili & Zulu Flow** — "Sawubona" (we see you), "Pamoja" (together), "Chagua" (choose)

## Requirements

- **Node.js** 18 or higher (for Electron)
- **Python** 3.7 or higher
- **pip** (Python package manager)
- **ffmpeg** (for audio extraction and video merging — [download here](https://ffmpeg.org/download.html))

## Installation

### 1. Clone this project

```bash
git clone https://github.com/jocysite/YouTube-Downloader.git
cd YouTube-Downloader
```

### 2. Install Python dependencies

```bash
pip install flask yt_dlp
```

### 3. Install Node.js dependencies

```bash
npm install
```

### 4. Install FFmpeg (required)

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Add `ffmpeg.exe` to your system PATH, or place it in the project directory

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

## Running the Application

### Development Mode

```bash
npm start
```

This will launch the **Afriway Downloader** desktop window with the Flask backend running in the background.

### Building for Distribution

To create an installer for your platform:

**Windows:**
```bash
npm run dist:win
```

**macOS:**
```bash
npm run dist:mac
```

**Linux:**
```bash
npm run dist:linux
```

The installer will be generated in the `dist/` folder.

## Project Structure

```
YouTube-Downloader/
├── main.js              # Electron main process (desktop entry point)
├── preload.js           # Electron preload script (secure bridge)
├── package.json         # Node.js project configuration
├── app.py               # Flask backend (Python server)
├── download.py          # Download utility functions
├── static/              # Frontend assets
│   ├── script.js       # JavaScript functionality
│   ├── style.css       # African-themed stylesheet
│   ├── style-dark.css  # Dark theme
│   └── style-light.css # Light theme
└── templates/           # HTML templates
    └── index.html      # Main application interface
```

## How It Works

1. **Electron** starts the **Flask** Python backend server automatically
2. The desktop window loads the web interface from the local Flask server
3. Paste a YouTube URL → Fetch metadata → Choose quality → Download
4. When you close the window, both Electron and Flask shut down cleanly

## The African Flow 🇪🇹

Each step in the workflow is named in Swahili or Zulu, celebrating the spirit of Africa:

| Step | Name | Meaning |
|------|------|---------|
| 1 | **Sawubona** | "We see you" (Zulu) — Enter URL |
| 2 | **Pamoja** | "Together" (Swahili) — Review details |
| 3 | **Chagua** | "Choose" (Swahili) — Select type |
| 4 | **Ubora** | "Quality" (Swahili) — Pick format |
| 5 | **Umoja** | "Unity" (Swahili) — Select playlist items |
| 6 | **Pakua** | "Download" (Swahili) — Start download |

## Usage

1. **Launch the app** using `npm start`
2. **Paste** a YouTube video or playlist URL into the input field
3. **Click "Fetch URL"** to retrieve video information and available formats
4. **Select** your preferred video quality and audio format
5. For playlists, choose which videos to include/exclude
6. **Click "Pakua Sasa (Download Now)"** to begin downloading
7. Track progress in real-time

## Troubleshooting

- **"Python not found" error**: Make sure Python is installed and added to your system PATH
- **"flask not found"**: Run `pip install flask yt_dlp`
- **FFmpeg errors**: Download and install FFmpeg, or verify it's in your PATH
- **Download fails**: Check your internet connection and ensure the YouTube URL is valid
- **Port conflict**: The app automatically finds a free port, so this shouldn't occur

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Desktop Wrapper:** Electron
- **Backend:** Python Flask
- **Download Engine:** yt-dlp
- **Theme:** Ethiopian & Pan-African inspired palette

## License

MIT

---

*Built with ❤️ using Electron, Flask, and yt-dlp*
*Design inspired by the colours of Ethiopia, Kenya, and the Pan-African spirit.*