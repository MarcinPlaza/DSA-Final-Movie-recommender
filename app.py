import pandas as pd
from flask import Flask, request, render_template
import time

from src.treestructure import MovieDatabase as TreeMovieDatabase, process_row as tree_process_row
from src.movie_dict import MovieDict, process_row as dict_process_row

# Initialize Flask app
app = Flask(__name__)

# Initialize both databases
tree_db = TreeMovieDatabase()
dict_db = MovieDict()

# Load and populate the databases
file_path = "data/10k-50k_movie_data_tmbd.csv"
chunk_size = 500  # Process in chunks

# Populate Tree structure database
for chunk in pd.read_csv(file_path, sep='|', on_bad_lines='skip', chunksize=chunk_size):
    filtered_chunk = chunk[['genres', 'directors', 'cast', 'vote_average', 'title']]
    for _, row in filtered_chunk.iterrows():
        movie = tree_process_row(row)
        if movie:
            tree_db.insert_movie(movie)

# Populate Dictionary-based database
data = pd.read_csv(file_path, sep='|', on_bad_lines='skip')
filtered_data = data[['genres', 'directors', 'cast', 'vote_average', 'title']]
for _, row in filtered_data.iterrows():
    movie = dict_process_row(row)
    if movie:
        dict_db.add_movie(movie)

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    genre = request.form.get('genre', '').strip()
    director = request.form.get('director', '').strip()
    lead_actor = request.form.get('lead_actor', '').strip()
    algorithm = request.form.get('algorithm', '').strip()

    # Choose the algorithm and database
    if algorithm == 'Tree Structure':
        db = tree_db
    elif algorithm == 'Dictionary of Lists':
        db = dict_db
    else:
        return "<h2>Error: Invalid algorithm selected.</h2>"

    # Measure the execution time
    start_time = time.time()
    results = db.find_similar_movies(
        genre=genre if genre else None,
        director=director if director else None,
        lead_actor=lead_actor if lead_actor else None
    )
    elapsed_time = time.time() - start_time

    # Format results for display
    formatted_results = [{'rank': i + 1, 'title': movie.title, 'rating': movie.imdb_rating} for i, movie in enumerate(results)]

    return render_template('results.html', results=formatted_results, elapsed_time=elapsed_time, algorithm=algorithm)

if __name__ == '__main__':
    app.run(debug=True)
