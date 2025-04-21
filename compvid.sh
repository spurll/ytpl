echo ffmpeg -i \"$1\" -c:v libx264 -pix_fmt yuv420p -crf 28 \"${1%.*}-compressed.mp4\"
ffmpeg -i "$1" -c:v libx264 -pix_fmt yuv420p -crf 28 "${1%.*}-compressed.mp4"
