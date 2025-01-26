#!/usr/bin/env python3
"""
Fetch full size movie poster from IMDB and to store it to current working directory.

Example: python3 imdb-movies-get-poster.py -n "1975 Barry Lydon" --filename barry-lydon-poster.jpg

"""

import argparse
import os
import requests
from imdb import IMDb

__author__ = "Mikko Tarvainen"
__version__ = "0.0.1"
__license__ = "MIT"

def main(args):
    ia = IMDb()
    search_results = ia.search_movie(args.movie_name)
    movie_obj = search_results[0] if search_results else None
    movie_poster_url = movie_obj.get_fullsizeURL() if movie_obj else None
    if not movie_poster_url:
        print(f"Poster for movie_title'{ args.movie_name }' not found.")
        return False
    else:
        poster_filename = os.path.splitext(args.filename)[0] # Remove file extension
        poster_filename_extension = os.path.splitext(movie_poster_url)[1] # Get file extension from URL
        poster_save_path = download_image_from_url(
            image_url = movie_poster_url,
            save_path = os.path.join(os.getcwd(), poster_filename + poster_filename_extension),
            force = args.force
        )
        output = {
            "movie_title": movie_obj['title'],
            "movie_year": movie_obj['year'],
            "movie_poster": poster_save_path
        }
        print(output)
        return True

def download_image_from_url(image_url, save_path, force=False):
    if (os.path.exists(save_path)) and force:
        os.remove(save_path)
    if (os.path.exists(save_path)):
        return save_path
    if image_url:
        # Define headers to mimic a Mozilla browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(image_url, headers=headers)
        with open(save_path, 'wb') as file:
            file.write(response.content)
            return save_path
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--movie-name", dest="movie_name", help="Name of the movie eg. 1975 Barry Lydon", action="store", required=True)
    parser.add_argument("--filename", dest="filename", help="Poster filename", action="store", default='poster.jpg')
    parser.add_argument("-f", "--force", dest="force", help="Regenerate new version and overwrite old", action="store_true", default=False)
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))
    args = parser.parse_args()
    main(args)