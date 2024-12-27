#!/usr/bin/env python3

# Written by Gem Newman. This work is licenced under the MIT License.
# Requires that both github.com/spurll/tracknum and github.com/spurll/normalize
# are installed and available on path.


from argparse import ArgumentParser
# from youtube_dl import YoutubeDL
# from youtube_dl.utils import DownloadError
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
import os.path as path


retries = 20
playlist_index = 1
current_path = path.dirname(path.realpath(__file__))

# Allow age-restricted videos (cookies.txt must be in the script directory)
cookies = path.join(current_path, 'cookies.txt')


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
    'cookiefile': cookies if path.isfile(cookies) else None,
    'progress_hooks': [track_playlist_index],
    'postprocessors': [
        {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'},
        {'key': 'FFmpegMetadata'},
        {'key': 'EmbedThumbnail'},
        {'key': 'ExecAfterDownload', 'exec_cmd': 'tracknum -f {}'},
        {'key': 'ExecAfterDownload', 'exec_cmd': 'normalize {} -v'}
    ]
}


def main():
    parser = ArgumentParser(
        description='Downloads the specified file or playlist from YouTube, '
        'extracts the audio, performs peak normalization, and sets ID3 track '
        'numbers based on its playlist index.')
    parser.add_argument('url', nargs='+', help='The URL(s) to download.')
    parser.add_argument('-s', '--start', nargs='?', help='The playlist index '
        'at which to begin downloading. Defaults to 1.', type=int, default=1)
    parser.add_argument('-e', '--end', nargs='?', help='The playlist index '
        'of the last track to download. Defaults to playlist end.', type=int,
        default=None)
    args = parser.parse_args()

    global retries
    global playlist_index
    success = False
    options['playliststart'] = args.start
    options['playlistend'] = args.end
    playlist_index = args.start

    # Download files
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
