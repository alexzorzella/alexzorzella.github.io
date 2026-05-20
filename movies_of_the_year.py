from pathlib import Path
import requests

import csv
import imdb
from colorama import Fore, Style

from baklava import is_null_or_whitespace, get_int_input

MOVIE_POSTER_DIR = "/public/movie_posters"
MOVIES_OF_THE_YEAR_TSV = "movies_of_the_year.tsv"

def main():
    movie_dir = Path(MOVIE_POSTER_DIR)

    movie_dir.mkdir(parents=True, exist_ok=True)

    total_images_downloaded = 0

    with open(MOVIES_OF_THE_YEAR_TSV, "r", encoding="utf-8", newline='\n') as file:
        reader = csv.reader(file, delimiter="\t")

        for row in reader:
            if len(row) < 2:
                continue

            movie_name = row[1]

            if is_null_or_whitespace(movie_name):
                continue

            access = imdb.IMDb()
            search_results = access.search_movie(movie_name)

            if search_results is None or len(search_results) < 1:
                print(f"{Fore.RED}No movie(s) named {movie_name} found{Style.RESET_ALL}")
                continue

            movie = search_results[0]

            if len(search_results) > 1:
                print(f"{Fore.MAGENTA}Found {len(movie)} results for {movie_name}.{Style.RESET_ALL}")

                for i, search_result in enumerate(search_results):
                    print(f"{i + 1}. {search_result['title']}")

                choice = get_int_input(prompt=f"{Fore.GREEN}Please select one:{Style.RESET_ALL} ", min=1, max=len(search_results))
                movie = search_results[choice]
                print(f"You chose {movie['title']}")

            movie_title = movie['title']
            movie_poster_url = movie['cover url']

            print(f"Downloading {Fore.CYAN}{movie_title}{Style.RESET_ALL}'s movie poster from {Fore.GREEN}{movie_poster_url}{Style.RESET_ALL}")

            try:
                image_data = requests.get(movie_poster_url).content

                with open(Path(MOVIE_POSTER_DIR) / f"{movie_title}_poster.jpg", "wb") as image:
                    image.write(image_data)
            except:
                print(f"{Fore.RED}Failed to download {search_results[0]['title']}{Style.RESET_ALL}'s movie poster")
                continue

            total_images_downloaded += 1

    print(f"Downloaded {total_images_downloaded} movie posters")

if __name__ == "__main__":
    main()