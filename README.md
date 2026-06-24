# YouTube Downloader

A web-based application for downloading YouTube videos and playlists with customizable quality and format options.

## Features

- Download individual YouTube videos
- Download entire playlists
- Choose from multiple video quality options
- Select preferred audio/video format combinations
- Save downloads to your Downloads folder or custom location
- Web-based user interface for easy access

## Requirements

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. **Clone or download this project** to your local machine

2. **Navigate to the project directory**:

   ```bash
   cd YouTube-Downloader-main
   ```

3. **Install required packages**:

   ```bash
   pip install flask yt_dlp
   ```

   Or if you prefer to install from a requirements file, you can create one:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask server**:

   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:

   ```
   http://localhost:5000
   ```

3. **Use the interface** to:
   - Paste a YouTube video or playlist URL
   - Select your preferred video quality and format
   - Click download to start the download

4. **Stop the server** by pressing `Ctrl+C` in the terminal

## Project Structure

```
YouTube-Downloader-main/
├── app.py              # Flask backend application
├── download.py         # Download utility functions
├── static/             # Frontend assets
│   ├── script.js      # JavaScript functionality
│   ├── style.css      # Main stylesheet
│   ├── style-dark.css # Dark theme
│   └── style-light.css # Light theme
└── templates/          # HTML templates
    └── index.html     # Main web interface
```

## Dependencies

- **flask**: Web framework for the backend server
- **yt_dlp**: Python library for downloading videos from YouTube and other platforms

## Notes

- Downloaded files are saved to your system's Downloads folder by default
- You can optionally specify a custom download location when prompted
- Ensure you have permission to download content and respect copyright laws
- The application requires an internet connection to function

## Troubleshooting

- **Port 5000 already in use**: Change the port in `app.py` by modifying the `app.run()` call
- **Module not found error**: Make sure all dependencies are installed with `pip install flask yt_dlp`
- **Download fails**: Check your internet connection and ensure the YouTube URL is valid

## License

Please refer to the original project license if available.
