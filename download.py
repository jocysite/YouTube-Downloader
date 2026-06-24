"""
Module to download YouTube videos and playlists by choosing from a list of available qualities.
"""
import yt_dlp
import os


def ask_download_location():
    """Ask user if they want to specify a custom download location."""
    use_custom = input(
        "\nUse custom download location? (y/n, default: current folder): ").strip().lower()

    if use_custom == 'y':
        location = input(
            "Enter download path (e.g., C:/Downloads or /home/user/Music): ").strip()
        if location and os.path.exists(location):
            return location
        else:
            print("Invalid path. Using current directory.")
            return "."
    return "."


def get_format_lists(url):
    """Extracts and categorizes available formats."""
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_options = []
        audio_options = []

        for f in info['formats']:
            # Filter for video-only streams
            if f.get('vcodec') != 'none' and f.get('acodec') == 'none':
                video_options.append({
                    'id': f['format_id'],
                    'ext': f['ext'],
                    'res': f.get('resolution', 'N/A'),
                    'note': f.get('format_note', '')
                })
            # Filter for audio-only streams
            elif f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                audio_options.append({
                    'id': f['format_id'],
                    'ext': f['ext'],
                    'abr': f.get('abr', 'N/A'),
                    'note': f.get('format_note', '')
                })

        return info.get('title'), video_options, audio_options


def present_menu(title, options, media_type="Video"):
    """Displays a numbered menu and returns the selected format ID."""
    print(f"\n--- Select {media_type} Quality for: {title} ---")

    for i, opt in enumerate(options, 1):
        detail = opt['res'] if media_type == "Video" else f"{opt['abr']}kbps"
        print(f"[{i}] {opt['ext'].upper()} - {detail} ({opt['note']})")

    while True:
        try:
            choice = int(
                input(f"Choose {media_type} option (1-{len(options)}): "))
            if 1 <= choice <= len(options):
                return options[choice - 1]['id']
        except (ValueError, IndexError):
            pass
        print("Invalid selection. Please enter a number from the list.")


def ask_download_type():
    """Ask user if they want video+audio or audio only."""
    print("\n--- Select Download Type ---")
    print("[1] Video + Audio (MP4)")
    print("[2] Audio Only (MP3/M4A)")

    while True:
        try:
            choice = int(input("Choose download type (1-2): "))
            if choice in [1, 2]:
                return choice
        except ValueError:
            pass
        print("Invalid selection. Please enter 1 or 2.")


def is_playlist(url):
    """Check if the URL is a playlist."""
    ydl_opts = {'quiet': True, 'extract_flat': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info.get('_type') == 'playlist'
        except yt_dlp.utils.DownloadError:
            return False


def get_playlist_info(url):
    """Get playlist title and video count."""
    ydl_opts = {'quiet': True, 'extract_flat': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('title', 'Unknown Playlist'), len(info.get('entries', []))


def download_playlist(url, download_type, download_path, selected_v_id=None, selected_a_id=None):
    """Download entire playlist with selected quality."""
    output_template = os.path.join(
        download_path, '%(playlist)s', '%(playlist_index)s - %(title)s.%(ext)s')

    if download_type == 1:  # Video + Audio
        ydl_opts = {
            'format': f'{selected_v_id}+{selected_a_id}',
            'merge_output_format': 'mp4',
            'outtmpl': output_template,
            'ignoreerrors': True,
            'no_warnings': False,
        }
    else:  # Audio only
        ydl_opts = {
            'format': selected_a_id,
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ignoreerrors': True,
            'no_warnings': False,
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("\nDownloading playlist...")
        ydl.download([url])

    print("\nPlaylist download complete!")
    print(f"📁 Location: {os.path.abspath(download_path)}")


def download_single_video(url, download_type, download_path, selected_v_id=None, selected_a_id=None):
    """Download a single video with selected quality."""
    if download_type == 1:  # Video + Audio
        output_template = os.path.join(
            download_path, '%(title)s_selected.%(ext)s')
        ydl_opts = {
            'format': f'{selected_v_id}+{selected_a_id}',
            'merge_output_format': 'mp4',
            'outtmpl': output_template,
        }
    else:  # Audio only
        output_template = os.path.join(
            download_path, '%(title)s_audio.%(ext)s')
        ydl_opts = {
            'format': selected_a_id,
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("\nDownloading your selection...")
        ydl.download([url])

    print("\nDownload complete successfully!")
    print(f"📁 Location: {os.path.abspath(download_path)}")


def download_selected_media(url):
    """Main flow to fetch, select, and download."""
    try:
        # Ask for download location
        download_path = ask_download_location()

        # Ask for download type
        download_type = ask_download_type()

        # Check if it's a playlist
        if is_playlist(url):
            playlist_title, video_count = get_playlist_info(url)
            print(
                f"\n🎵 Playlist detected: '{playlist_title}' ({video_count} videos)")
            print(
                f"📁 Will be saved to: {os.path.abspath(download_path)}/{playlist_title}/")

            # Ask user if they want to proceed
            proceed = input(
                "\nDownload entire playlist? (y/n): ").strip().lower()
            if proceed != 'y':
                print("Download cancelled.")
                return

            # Get format options from the first video in the playlist
            print("\nFetching format options from first video...")
            ydl_opts = {'quiet': True, 'extract_flat': False, 'playlistend': 1}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                first_video = info['entries'][0] if 'entries' in info else info

            title = first_video.get('title')
            video_options = []
            audio_options = []

            for f in first_video['formats']:
                if f.get('vcodec') != 'none' and f.get('acodec') == 'none':
                    video_options.append({
                        'id': f['format_id'],
                        'ext': f['ext'],
                        'res': f.get('resolution', 'N/A'),
                        'note': f.get('format_note', '')
                    })
                elif f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    audio_options.append({
                        'id': f['format_id'],
                        'ext': f['ext'],
                        'abr': f.get('abr', 'N/A'),
                        'note': f.get('format_note', '')
                    })

            if not audio_options:
                print("Could not find audio streams.")
                return

            if download_type == 1:  # Video + Audio
                if not video_options:
                    print("Could not find video streams.")
                    return
                selected_v_id = present_menu(title, video_options, "Video")
                selected_a_id = present_menu(title, audio_options, "Audio")
                print(
                    f"\nThis quality will be applied to all {video_count} videos in the playlist.")
                download_playlist(url, download_type,
                                  download_path, selected_v_id, selected_a_id)
            else:  # Audio only
                selected_a_id = present_menu(title, audio_options, "Audio")
                print(
                    f"\nThis audio quality will be applied to all {video_count} videos in the playlist.")
                download_playlist(url, download_type,
                                  download_path, selected_a_id=selected_a_id)

        else:
            # Single video download
            print("\n📹 Single video detected")
            print(f"📁 Will be saved to: {os.path.abspath(download_path)}/")

            title, v_list, a_list = get_format_lists(url)

            if not a_list:
                print("Could not find audio streams. Try a different URL.")
                return

            if download_type == 1:  # Video + Audio
                if not v_list:
                    print("Could not find video streams. Try a different URL.")
                    return
                selected_v_id = present_menu(title, v_list, "Video")
                selected_a_id = present_menu(title, a_list, "Audio")
                download_single_video(
                    url, download_type, download_path, selected_v_id, selected_a_id)
            else:  # Audio only
                selected_a_id = present_menu(title, a_list, "Audio")
                download_single_video(
                    url, download_type, download_path, selected_a_id=selected_a_id)

    except yt_dlp.utils.DownloadError as err:
        print(f"\nDownload error occurred: {err}")
    except KeyError as err:
        print(f"\nData extraction error: Missing key {err}")
    except Exception as err:
        print(f"\nUnexpected error: {err}")


if __name__ == "__main__":
    print("=" * 60)
    print("YouTube Video/Playlist Downloader")
    print("=" * 60)
    url_input = input("\nEnter YouTube URL (video or playlist): ").strip()
    if url_input:
        download_selected_media(url_input)
    else:
        print("No URL provided. Exiting.")
