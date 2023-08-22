#!/bin/bash
set -e
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

sh -x test-avi-to-mp4.sh
sh -x test-flac-to-mp3.sh

