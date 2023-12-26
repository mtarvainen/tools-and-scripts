#!/bin/bash
set -e
if ! [ -x "$(command -v wget)" ]; then
  echo 'Error: wget is not installed.'
  exit 1
fi
test -d ./tests/data/mp4 && rm -rf ./tests/data/mp4
wget --no-clobber -P ./tests/data \
    https://filesamples.com/samples/video/avi/sample_1280x720_surfing_with_audio.avi \
    https://filesamples.com/samples/video/avi/sample_960x400_ocean_with_audio.avi \
    https://filesamples.com/samples/video/avi/sample_960x540.avi

python3 media-converter.py -i avi -o mp4 --force
python3 media-converter.py -i avi -o mp4 -c 24 --force
