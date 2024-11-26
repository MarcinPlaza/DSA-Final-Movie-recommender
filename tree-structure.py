import pandas as pd
import ast  # for interpreting the json in the dataset
import time

# essentially node, (movie object)
class Movie:
    def __init__(self, title, genre, director, lead_actor, imdb_rating):
        self.title = title
        self.genre = genre
        self.director = director
        self.lead_actor = lead_actor
        self.imdb_rating = imdb_rating

    def __repr__(self):
        return f"{self.title} ({self.imdb_rating})"

# define the movie tree
class MovieDatabase:
    def __init__(self):
        # Root level of the hierarchy
        self.db = {}

    def insert_movie(self, movie):
        #insert movie into heirarchy
        genre = movie.genre
        director = movie.director
        lead_actor = movie.lead_actor

        # move through tree, if branch not present, make one
        if genre not in self.db:
            self.db[genre] = {}
        if director not in self.db[genre]:
            self.db[genre][director] = {}
        if lead_actor not in self.db[genre][director]:
            self.db[genre][director][lead_actor] = []
        
        # each leaf is a list of films sorted by movie rating (dont really expect this to ever be more than one unless a film has the same genre,director, and actor)
        self.db[genre][director][lead_actor].append(movie)
        self.db[genre][director][lead_actor].sort(key=lambda x: x.imdb_rating, reverse=True)

    def find_similar_movies(self, genre=None, director=None, lead_actor=None, max_results=10):
        start_time = time.time()
        """Find up to max_results movies, progressively relaxing the search criteria."""
        results = []

        # Helper to collect movies from a subtree
        def collect_movies(subtree):
            """Recursively collect movies from a subtree."""
            movies = []
            if isinstance(subtree, list):
                return subtree
            for key in subtree:
                movies.extend(collect_movies(subtree[key]))
            return movies

        # Search movies by progressively relaxing criteria
        try:
            # 1. Exact match: Genre > Director > Lead Actor
            if genre and director and lead_actor:
                current_level = self.db.get(genre, {}).get(director, {}).get(lead_actor, [])
                results.extend(current_level)

            # 2. Relax: Genre > Director
            if len(results) < max_results and genre and director:
                current_level = self.db.get(genre, {}).get(director, {})
                if isinstance(current_level, dict):  # Ensure it's a subtree
                    results.extend(collect_movies(current_level))

            # 3. Relax: Genre only
            if len(results) < max_results and genre:
                current_level = self.db.get(genre, {})
                if isinstance(current_level, dict):  # Ensure it's a subtree
                    results.extend(collect_movies(current_level))

            # 4. Global: All movies
            if len(results) < max_results:
                results.extend(collect_movies(self.db))

        except KeyError:
            # No match found
            pass

        # Deduplicate and limit results
        seen = set()
        unique_results = []
        for movie in results:
            if len(unique_results) >= max_results:
                break
            if movie not in seen:
                seen.add(movie)
                unique_results.append(movie)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"\nTime taken to find closest movies: {elapsed_time:.6f} seconds")

        return unique_results


    def _collect_movies(self, subtree):
        #recursive subtree search
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

############################### loading dataset into program ###########################################
db = MovieDatabase()

# csv we got had pipe separator (pipe '|')
file_path = "8000_movie_data_tmbd.csv" 

# read file in chunks cuz my loptop didn't have enough ram
chunk_size = 500  

# deal with json from dataset
def parse_json_string(value):
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return []

# Function to extract the first genre, first director, and lead actor
def process_row(row):
    try:
        genres = parse_json_string(row['genres'])
        genre = genres[0]['name'] if genres and isinstance(genres, list) and 'name' in genres[0] else 'Unknown'
        
        directors = parse_json_string(row['directors'])
        director = directors[0]['name'] if directors and isinstance(directors, list) and 'name' in directors[0] else 'Unknown'
        
        cast = parse_json_string(row['cast'])
        lead_actor = cast[0]['name'] if cast and isinstance(cast, list) and 'name' in cast[0] else 'Unknown'
        
        imdb_rating = float(row['vote_average']) if pd.notna(row['vote_average']) else 0.0
        
        title = row['title'] if pd.notna(row['title']) else "Unknown Title"
        
        return Movie(title, genre, director, lead_actor, imdb_rating)
    except Exception as err:
        print(f"Error processing row: {row}, Error: {err}")
        return None

for chunk in pd.read_csv(
    file_path, 
    sep='|', 
    on_bad_lines='skip', 
    chunksize=chunk_size,  # chunk loading
    low_memory=True
):

    filtered_chunk = chunk[['genres', 'directors', 'cast', 'vote_average', 'title']]

    for _, row in filtered_chunk.iterrows():
        movie = process_row(row)
        if movie:
            db.insert_movie(movie)

# Example queries
print("\nComedy movies ")
print(db.find_similar_movies( genre="Science Fiction", director="Jeremy Kagan", lead_actor="Kyle MacLachlan"))

#call to get similar movies db.find_similar_movies( genre="Science Fiction", director="Jeremy Kagan", lead_actor="Kyle MacLachlan")
#returns array of "title (rating)" of 10 films also just prints the time it took
