#!/usr/bin/env python3

# Written by Gem Newman. This work is licenced under the MIT License.
# Requires that github.com/spurll/tracknum is installed and available on path.


from argparse import ArgumentParser
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError


retries = 20
playlist_index = 1


def track_playlist_index(d):
    # Keep track of successful downloads to allow resuming in case of error
    global playlist_index
    if d['status'] == 'finished':
        playlist_index += 1


options = {
    'outtmpl': '%(playlist_index)s %(title)s.%(ext)s',
    'outtmpl_na_placeholder': '0',
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'continuedl': True,
    'progress_hooks': [track_playlist_index],
    'postprocessors': [
        {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'},
        {'key': 'FFmpegMetadata'},
        {'key': 'EmbedThumbnail'},
        {'key': 'ExecAfterDownload', 'exec_cmd': 'tracknum -f {}'}
    ]
}


def main():
    parser = ArgumentParser(
        description='Downloads the specified file or playlist from YouTube, '
        'extracts the audio, and sets ID3 track numbers based on its '
        'playlist index.')
    parser.add_argument("url", nargs='+', help='The URL(s) to download.')
    args = parser.parse_args()

    global retries
    success = False

    while not success and retries >= 0:
        try:
            with YoutubeDL(options) as ytdl:
                ytdl.download(args.url)
                success = True
        except DownloadError:
            # Attempt to resume after the last successful download
            print(f'Download failed. Retrying {retries} more times.')
            retries -= 1
            options['playliststart'] = playlist_index


if __name__ == "__main__":
    main()
