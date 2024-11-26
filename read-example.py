import pandas as pd
import ast  # For safely evaluating string representations of Python literals

# Define the Movie class
class Movie:
    def __init__(self, title, genre, director, lead_actor, imdb_rating):
        self.title = title
        self.genre = genre
        self.director = director
        self.lead_actor = lead_actor
        self.imdb_rating = imdb_rating

    def __repr__(self):
        return f"{self.title} ({self.imdb_rating})"

# Define the MovieDatabase class
class MovieDatabase:
    def __init__(self):
        # Root level of the hierarchy
        self.db = {}

    def insert_movie(self, movie):
        """Insert a movie into the hierarchical structure."""
        genre = movie.genre
        director = movie.director
        lead_actor = movie.lead_actor

        # Navigate or create levels in the hierarchy
        if genre not in self.db:
            self.db[genre] = {}
        if director not in self.db[genre]:
            self.db[genre][director] = {}
        if lead_actor not in self.db[genre][director]:
            self.db[genre][director][lead_actor] = []
        
        # Append the movie to the list sorted by IMDb rating
        self.db[genre][director][lead_actor].append(movie)
        self.db[genre][director][lead_actor].sort(key=lambda x: x.imdb_rating, reverse=True)

    def find_similar_movies(self, genre=None, director=None, lead_actor=None):
        """Find movies matching the given criteria."""
        results = []
        current_level = self.db

        try:
            if genre:
                current_level = current_level[genre]
            if director:
                current_level = current_level[director]
            if lead_actor:
                current_level = current_level[lead_actor]

            # If we reach a list of movies, return it
            if isinstance(current_level, list):
                results = current_level
            else:
                # Collect all movies in the subtree
                results = self._collect_movies(current_level)
        except KeyError:
            # No match found
            pass

        return results

    def _collect_movies(self, subtree):
        """Recursively collect all movies from a subtree."""
        movies = []
        if isinstance(subtree, list):
            return subtree
        for key in subtree:
            movies.extend(self._collect_movies(subtree[key]))
        return movies

    def display(self):
        """Display the structure for debugging."""
        from pprint import pprint
        pprint(self.db)

# Load data and populate the database
db = MovieDatabase()

# Load the CSV file with the correct separator (pipe '|')
file_path = "cleaned_movie_data_tmbd.csv"  # Replace with your CSV file path
data = pd.read_csv(file_path, sep='|', on_bad_lines='skip')

# Check the columns to ensure they match the dataset
print("Columns in the dataset:", data.columns)

# Filter relevant columns
filtered_data = data[['genres', 'directors', 'cast', 'vote_average', 'title']]

# Helper function to process JSON-like strings safely
def parse_json_string(value):
    try:
        # Safely evaluate JSON-like strings
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return []

# Helper function to extract the first genre, first director, and lead actor
def process_row(row):
    try:
        # Parse genres
        genres = parse_json_string(row['genres'])
        genre = genres[0]['name'] if genres and isinstance(genres, list) and 'name' in genres[0] else 'Unknown'
        
        # Parse directors
        directors = parse_json_string(row['directors'])
        director = directors[0]['name'] if directors and isinstance(directors, list) and 'name' in directors[0] else 'Unknown'
        
        # Parse cast
        cast = parse_json_string(row['cast'])
        lead_actor = cast[0]['name'] if cast and isinstance(cast, list) and 'name' in cast[0] else 'Unknown'
        
        # Get IMDb rating
        imdb_rating = float(row['vote_average']) if pd.notna(row['vote_average']) else 0.0
        
        # Get movie title
        title = row['title'] if pd.notna(row['title']) else "Unknown Title"
        
        return Movie(title, genre, director, lead_actor, imdb_rating)
    except Exception as e:
        print(f"Error processing row: {row}, Error: {e}")
        return None

# Process each row and add to the database
for _, row in filtered_data.iterrows():
    movie = process_row(row)
    if movie:
        db.insert_movie(movie)

# Display the database structure
#db.display()

# Example queries
print("\nComedy movies by Jean Renoir:")
print(db.find_similar_movies(genre="Comedy", director="Jean Renoir"))

print("\nMovies starring Jean-Pierre Cassel:")
print(db.find_similar_movies(lead_actor="Jean-Pierre Cassel"))
