"""
Flask backend for YouTube Downloader
"""
import logging
import os
import sys
import threading
import uuid
from pathlib import Path

import yt_dlp
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Disable Flask request logging for cleaner console
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Store download sessions
download_sessions = {}


def get_downloads_folder():
    """Get the user's Downloads folder path"""
    if os.name == 'nt':  # Windows
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:  # macOS and Linux
        return str(Path.home() / "Downloads")


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/fetch-info', methods=['POST'])
def fetch_info():
    """Fetch video/playlist information"""
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        print(f"\n🔍 Fetching info for: {url}")

        # Check if playlist
        ydl_opts = {'quiet': True, 'extract_flat': 'in_playlist'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            is_playlist = info.get('_type') == 'playlist'

        if is_playlist:
            playlist_title = info.get('title', 'Unknown Playlist')
            entries = info.get('entries', [])

            # Build video list
            videos = []
            for idx, entry in enumerate(entries):
                if entry:
                    videos.append({
                        'index': idx + 1,
                        'id': entry.get('id', ''),
                        'title': entry.get('title', f'Video {idx + 1}'),
                        'duration': entry.get('duration', 0),
                        'url': entry.get('url', '') or f"https://www.youtube.com/watch?v={entry.get('id', '')}"
                    })

            print(f"📁 Playlist: {playlist_title} ({len(videos)} videos)")

            # Get first video info for formats
            ydl_opts = {'quiet': True, 'extract_flat': False, 'playlistend': 1}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                first_video = info['entries'][0] if 'entries' in info else info

            formats = first_video['formats']
            title = playlist_title
            video_count = len(videos)
        else:
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info['formats']
                title = info.get('title', 'Unknown')
            video_count = 1
            videos = []
            print(f"🎥 Video: {title}")

        # Extract video and audio formats
        video_formats = []
        audio_formats = []

        for f in formats:
            if f.get('vcodec') != 'none' and f.get('acodec') == 'none':
                video_formats.append({
                    'id': f['format_id'],
                    'ext': f['ext'],
                    'res': f.get('resolution', 'N/A'),
                    'note': f.get('format_note', ''),
                    'height': f.get('height', 0)
                })
            elif f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                audio_formats.append({
                    'id': f['format_id'],
                    'ext': f['ext'],
                    'abr': f.get('abr', 0),
                    'note': f.get('format_note', '')
                })

        # Sort by quality
        video_formats.sort(key=lambda x: x['height'], reverse=True)
        audio_formats.sort(key=lambda x: x['abr'], reverse=True)

        print(
            f"✅ Found {len(video_formats)} video formats and {len(audio_formats)} audio formats\n")

        return jsonify({
            'success': True,
            'title': title,
            'is_playlist': is_playlist,
            'video_count': video_count,
            'videos': videos,
            'video_formats': video_formats,
            'audio_formats': audio_formats
        })

    except yt_dlp.utils.DownloadError as e:
        print(f"❌ Error: {str(e)}\n")
        return jsonify({'error': str(e)}), 500
    except (KeyError, ValueError) as e:
        print(f"❌ Data extraction error: {str(e)}\n")
        return jsonify({'error': f'Data extraction error: {str(e)}'}), 500


@app.route('/api/download', methods=['POST'])
def download():
    """Start download process"""
    try:
        data = request.json
        url = data.get('url')
        download_type = data.get('download_type')
        video_format_id = data.get('video_format_id')
        audio_format_id = data.get('audio_format_id')
        is_playlist = data.get('is_playlist', False)
        # NEW: List of indices to skip
        skip_indices = data.get('skip_indices', [])

        if not url or not audio_format_id:
            return jsonify({'error': 'Missing required parameters'}), 400

        # Create session ID
        session_id = str(uuid.uuid4())
        download_sessions[session_id] = {
            'status': 'downloading',
            'progress': 0,
            'message': 'Starting download...'
        }

        print(f"\n🚀 Starting download...")
        print(f"📥 Type: {download_type.upper()}")
        print(f"🔗 URL: {url}")
        if skip_indices:
            print(f"⏭️  Skipping videos: {skip_indices}")
        print()

        # Start download in background thread
        thread = threading.Thread(
            target=_download_thread,
            args=(session_id, url, download_type, video_format_id,
                  audio_format_id, is_playlist, skip_indices)
        )
        thread.daemon = True
        thread.start()

        return jsonify({
            'success': True,
            'session_id': session_id
        })

    except (ValueError, KeyError) as e:
        print(f"❌ Error: {str(e)}\n")
        return jsonify({'error': str(e)}), 500


@app.route('/api/download-status/<session_id>', methods=['GET'])
def download_status(session_id):
    """Get download status"""
    session = download_sessions.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404

    return jsonify(session)


def _download_thread(session_id, url, download_type, video_format_id, audio_format_id, is_playlist, skip_indices):
    """Background thread for downloading with smart quality fallback"""
    try:
        # Use system Downloads folder
        download_path = get_downloads_folder()

        # Create YouTube Downloads subfolder
        youtube_folder = os.path.join(download_path, 'YouTube Downloads')
        os.makedirs(youtube_folder, exist_ok=True)

        if is_playlist:
            output_template = os.path.join(
                youtube_folder,
                '%(playlist)s',
                '%(playlist_index)s - %(title)s.%(ext)s'
            )
        else:
            output_template = os.path.join(youtube_folder, '%(title)s.%(ext)s')

        last_video_percent = -1
        last_audio_percent = -1
        current_stage = None
        current_playlist_index = 0

        def progress_hook(d):
            """Handle download progress with clean console output"""
            nonlocal last_video_percent, last_audio_percent, current_stage, current_playlist_index

            if d['status'] == 'downloading':
                try:
                    # Get percentage
                    percent_str = d.get(
                        '_percent_str', '0%').strip().replace('%', '')
                    try:
                        percent = float(percent_str)
                    except ValueError:
                        percent = 0

                    # Get playlist info if available
                    info_dict = d.get('info_dict', {})
                    playlist_index = info_dict.get('playlist_index')

                    if playlist_index and playlist_index != current_playlist_index:
                        current_playlist_index = playlist_index
                        if current_playlist_index in skip_indices:
                            print(
                                f"\n⏭️  Skipping video {current_playlist_index}")
                            return
                        print(
                            f"\n📥 Downloading video {current_playlist_index}...")
                        # Reset percentages for new video
                        last_video_percent = -1
                        last_audio_percent = -1

                    # Determine stage
                    filename = d.get('filename', '')

                    if 'f' + str(video_format_id) in filename or (download_type == 'video' and current_stage != 'audio'):
                        stage = 'video'
                    else:
                        stage = 'audio'

                    # Only print if percentage increased
                    if stage == 'video' and download_type == 'video':
                        if int(percent) > int(last_video_percent):
                            last_video_percent = percent
                            current_stage = 'video'
                            sys.stdout.write(f"\r🎬 Video: {percent:.1f}% ")
                            sys.stdout.flush()
                    elif stage == 'audio' or download_type == 'audio':
                        if int(percent) > int(last_audio_percent):
                            last_audio_percent = percent
                            current_stage = 'audio'
                            if download_type == 'video' and last_video_percent > 0:
                                print()
                            sys.stdout.write(f"\r🎵 Audio: {percent:.1f}% ")
                            sys.stdout.flush()

                    # Update session
                    download_sessions[session_id]['progress'] = percent
                    download_sessions[session_id]['message'] = f"Downloading... {percent:.1f}%"

                except (ValueError, KeyError):
                    pass

            elif d['status'] == 'finished':
                if last_video_percent > 0 or last_audio_percent > 0:
                    print()
                print("⚙️  Processing and merging...")
                download_sessions[session_id]['message'] = 'Processing and merging...'

        # Create match filter for skipping videos
        def match_filter(info_dict, incomplete):
            """Filter to skip specific playlist items"""
            if is_playlist and skip_indices:
                playlist_index = info_dict.get('playlist_index')
                if playlist_index in skip_indices:
                    print(
                        f"⏭️  Skipping video {playlist_index}: {info_dict.get('title', 'Unknown')}")
                    return "Skipped by user"
            return None

        # Build comprehensive format string with multiple fallbacks
        if download_type == 'video':
            format_string = (
                f'{video_format_id}+{audio_format_id}/'  # Try exact formats
                # Selected video + best audio
                f'{video_format_id}+bestaudio/'
                # Best video + selected audio
                f'bestvideo+{audio_format_id}/'
                # Quality limits
                f'bestvideo[height<=1080]+bestaudio[abr>=96]/'
                f'bestvideo+bestaudio/'                   # Best of both
                f'best'                                    # Final fallback
            )

            print(
                f"🎯 Targeting: Video format {video_format_id} + Audio format {audio_format_id}")
            print(f"📋 Smart quality fallback enabled\n")

            ydl_opts = {
                'format': format_string,
                'merge_output_format': 'mp4',
                'outtmpl': output_template,
                'ignoreerrors': True,  # Continue on errors
                'progress_hooks': [progress_hook],
                'match_filter': match_filter,
                'noplaylist': not is_playlist,
                'quiet': False,
                'no_warnings': False,
            }
        else:  # audio only
            format_string = (
                f'{audio_format_id}/'      # Try selected
                f'bestaudio[abr>=128]/'    # Best audio >= 128kbps
                f'bestaudio/'               # Any best audio
                f'best'                     # Final fallback
            )

            print(f"🎯 Targeting: Audio format {audio_format_id}")
            print(f"📋 Smart quality fallback enabled\n")

            ydl_opts = {
                'format': format_string,
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ignoreerrors': True,  # Continue on errors
                'progress_hooks': [progress_hook],
                'match_filter': match_filter,
                'noplaylist': not is_playlist,
                'quiet': False,
                'no_warnings': False,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"\n✅ Download completed!")
        print(f"📁 Saved to: {youtube_folder}\n")

        download_sessions[session_id]['status'] = 'completed'
        download_sessions[session_id]['progress'] = 100
        download_sessions[session_id][
            'message'] = f'Download completed! Saved to: {youtube_folder}'

    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Download error: {str(e)}\n")
        download_sessions[session_id]['status'] = 'error'
        download_sessions[session_id]['message'] = f'Download error: {str(e)}'
    except (OSError, KeyError) as e:
        print(f"\n❌ Error: {str(e)}\n")
        download_sessions[session_id]['status'] = 'error'
        download_sessions[session_id]['message'] = f'Error: {str(e)}'


if __name__ == '__main__':
    # Use port from environment (set by Electron) or default to 5000
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', '1') == '1'

    print("\n" + "="*50)
    print("Afriway Downloader Server")
    print("="*50)
    print(f"Server running at: http://localhost:{port}")
    print("Downloads will be saved to:", get_downloads_folder())
    print("Proudly African - Inspired by Ethiopia")
    print("="*50 + "\n")

    app.run(debug=debug_mode, port=port, host='127.0.0.1')
