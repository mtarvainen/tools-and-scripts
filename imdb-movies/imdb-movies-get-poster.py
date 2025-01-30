#!/usr/bin/env python3
"""
Fetch full size movie poster from IMDB and to store it to current working directory.

Example: python3 imdb-movies-get-poster.py --input "1975 Barry Lydon" --output barry-lydon-poster.jpg

"""

import argparse
import imdb
import os
import requests
import urllib.parse

__author__ = "Mikko Tarvainen"
__version__ = "0.0.2"
__license__ = "MIT"

def main(args):
    ia = imdb.IMDb()

    # If movie name is '.', use the current directory name as the movie title
    if args.input == '.':
        args.input = os.path.basename(os.getcwd())
    search_results = ia.search_movie(args.input)
    movie_obj = search_results[0] if search_results else None
    movie_poster_url = movie_obj.get_fullsizeURL() if movie_obj else None
    if not movie_poster_url:
        print(f"Poster for movie title '{args.input}' not found.")
        return False
    else:
        poster_filename = os.path.splitext(os.path.basename(args.output))[0] # Remove file extension
        poster_filename_extension = os.path.splitext(urllib.parse.urlparse(movie_poster_url).path)[1] # Get file extension from URL
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
    if os.path.exists(save_path) and force:
        os.remove(save_path)
    if os.path.exists(save_path) and not force:
        return save_path
    if image_url:
        # Define headers to mimic a Mozilla browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(image_url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
                return save_path
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return False
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", help="Name of the movie eg. 1975 Barry Lydon. Value '.' uses the directory name as the movie title", action="store", required=True)
    parser.add_argument("-o", "--output", dest="output", help="Poster output filename (default: 'poster.jpg')", action="store", required=False, default='poster.jpg')
    parser.add_argument("-f", "--force", dest="force", help="Force download of a new poster even if the file already exists", action="store_true", default=False)
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s (version {__version__})")
    args = parser.parse_args()
    main(args)