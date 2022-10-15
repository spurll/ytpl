#!/usr/bin/env python3

# Written by Gem Newman. This work is licenced under the MIT License.
# Requires that github.com/spurll/tracknum is installed and available on path.


from argparse import ArgumentParser
from youtube_dl import YoutubeDL


OPTIONS = {
    'outtmpl': '%(playlist_index)s %(title)s.%(ext)s',
    'outtmpl_na_placeholder': '0',
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'continuedl': True,
    'retries': 100,
    'sleep_interval': 2,
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

    with YoutubeDL(OPTIONS) as ytdl:
        ytdl.download(args.url)


if __name__ == "__main__":
    main()
