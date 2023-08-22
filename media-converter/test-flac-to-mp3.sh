#!/bin/bash
set -e
test -d ./tests/data && rm -rf ./tests/data
git clone https://github.com/sfiera/flac-test-files.git ./tests/data
python3 media-converter.py -i flac -o mp3 --force
