import pandas as pd
import time
import ast


class Movie:
    def __init__(self, title, genres, director, lead_actor, imdb_rating):
        self.title = title
        self.genres = genres
        self.director = director
        self.lead_actor = lead_actor
        self.imdb_rating = imdb_rating

    def __repr__(self):
        return f"{self.title} ({self.imdb_rating})"

    def get_keyset(self):
        keys = set()
        keys.update(self.director)
        keys.update(self.lead_actor)
        keys.update(self.genres)  # Add all genres directly from the list
        return keys


class MovieDict:
    def __init__(self):
        self.dict = {}

    def add_movie(self, movie):
        # Loop through each key from the movie's keyset
        for key in movie.get_keyset():
            # Safely handle Unicode characters in the debug print statement
            try:
                print(f"Adding movie: {movie.title}, Keys: {movie.get_keyset()}")
            except UnicodeEncodeError:
                print(
                    f"Adding movie: {movie.title.encode('ascii', errors='replace').decode()}, Keys: {set(key.encode('ascii', errors='replace').decode() for key in movie.get_keyset())}")

            # If the key does not exist, initialize with an empty list
            if key not in self.dict:
                self.dict[key] = []

            # Add the movie to the list
            self.dict[key].append(movie)

    def find_similar_movies(self, genre=None, director=None, lead_actor=None, max_results=10):
        results = []

        # Score movies based on criteria
        scores = {}

        # Genre matching
        if genre:
            genre_movies = self.dict.get(genre, [])
            for movie in genre_movies:
                scores[movie] = scores.get(movie, 0) + 3  # Weight for genre

        # Director matching
        if director:
            director_movies = self.dict.get(director, [])
            for movie in director_movies:
                scores[movie] = scores.get(movie, 0) + 2  # Weight for director

        # Actor matching
        if lead_actor:
            actor_movies = self.dict.get(lead_actor, [])
            for movie in actor_movies:
                scores[movie] = scores.get(movie, 0) + 1  # Weight for actor

        # Sort movies by score, descending order, and take the top 'max_results'
        sorted_movies = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = [movie for movie, _ in sorted_movies[:max_results]]

        return results


def parse_json_string(value):
    try:
        return ast.literal_eval(value)
    except(ValueError, SyntaxError):
        return []


def process_row(row):
    try:
        # Parse genres and get the first genre
        genres = parse_json_string(row['genres'])
        genre = genres[0]['name'] if genres and isinstance(genres, list) and 'name' in genres[0] else 'Unknown'

        # Parse directors and get the first director
        directors = parse_json_string(row['directors'])
        director = [directors[0]['name']] if directors and isinstance(directors, list) and 'name' in directors[0] else [
            'Unknown']

        # Parse cast and get the first actor
        cast = parse_json_string(row['cast'])
        lead_actor = [cast[0]['name']] if cast and isinstance(cast, list) and 'name' in cast[0] else ['Unknown']

        # Safely parse the IMDb rating
        try:
            imdb_rating = float(row['vote_average']) if pd.notna(row['vote_average']) else 0.0
            if imdb_rating < 0.0 or imdb_rating > 10.0:
                imdb_rating = 0.0
        except ValueError:
            imdb_rating = 0.0
        # imdb_rating = float(row['vote_average']) if pd.notna(row['vote_average']) else 0.0
        # Get movie title
        title = row['title'] if pd.notna(row['title']) else "Unknown Title"

        return Movie(title, [genre], director, lead_actor, imdb_rating)
    except Exception as err:
        print(f"Error processing row: {row}, Error: {err}")
        return None