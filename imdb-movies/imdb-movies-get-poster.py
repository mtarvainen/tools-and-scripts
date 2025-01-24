#!/usr/bin/env python3
"""
Fetch full size movie poster from IMDB and to store it to current working directory.

Example: python3 imdb-movies-get-poster.py -n "1975 Barry Lydon" -f barry-lydon-poster.jpg

"""

import argparse
import os
import requests
from imdb import IMDb

__author__ = "Mikko Tarvainen"
__version__ = "0.0.1"
__license__ = "MIT"

def get_imdb_movie_object(movie_title):
    ia = IMDb()
    search_results = ia.search_movie(movie_title)
    if search_results:        
        return search_results[0] # Get the first result (most relevant)
    return False

def download_image(url, save_as):
    # Define headers to mimic a Mozilla browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    if (os.path.exists(save_as)):
        return save_as
    response = requests.get(url, headers=headers)
    with open(save_as, 'wb') as file:
        file.write(response.content)
        return save_as
    return False

def main(args):
    io = {
        'movie_name': args.movie_name,
        'filename': args.filename, # poster.jpg
    }
    movie = get_imdb_movie_object(io['movie_name'])
    poster_save_path = os.path.join(os.getcwd(), io['filename'])
    if movie:
        download_image(movie['full-size cover url'], poster_save_path)
        print(f"movie_title={ movie['title'] }, poster_save_path={ poster_save_path }")
    else:
        print(f"movie_name='{ io['movie_name'] }' not found")
        return False
    if args.stty_sane:
        os.system('stty sane')
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--movie-name", dest="movie_name", help="Name of the movie eg. 1975 Barry Lydon", action="store", required=True)
    parser.add_argument("-f", "--filename", dest="filename", help="Poster filename", action="store", default='poster.jpg')
    # parser.add_argument("-f", "--force", dest="force", help="Regenerate new version and overwrite old", action="store_true", default=False)
    parser.add_argument("--stty-sane", dest="stty_sane", help="Ensure optimal terminal line settings", action="store_true", default=True)
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))
    args = parser.parse_args()
    main(args)
