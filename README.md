
# CineMatch - A Movie Recommendation System

## Overview 

**CineMatch** is a Python-based project that helps users find movies or shows they'll enjoy. It utilizes a dynamic algorithm to calculate movie similarities and provides personalized recommendations based on various criteria like genre, director and more.

## Features

- Search by Genre, Director, and Lead Actor:
    - Genre is required; director and lead actor are optional.
- Two Distinct Algorithms:
    - Tree Structure: Organizes movies hierarchically for efficient exact-match searches.
    - Dictionary of Lists: Scores movies based on weighted criteria for more flexible recommendations.
- Top 10 Recommendations: Results ranked by relevance and IMDb rating.
- Execution Time: Displays how long the search took.
- User-Friendly Interface: Responsive web design for easy navigation.

## Usage
1. Home Page:
-   Enter a genre (e.g., "Comedy")
-   Optionally specify a director and/or lead actor.
-   Choose the search algorithm:
    -   Tree structure for hierarchical searches.
    -   Dictionary of Lists for flexible scoring.
-   Click Search to view recommendations.
2. Search Results:
-   Displays the top 10 recommendations, including:
    -   Movie Title
    -   IMDb rating
-   Shows the execution time for the search.
-   Click Search Again to return to the home page.

## How It Works
**Tree Structure**
- Movies are organized hierarchically:
    - Genre -> Director -> Lead Actor
- Searches prioritize exact matches at each level.
- Best suited for searches with specific inputs.

**Dictionary of Lists**
- Movies are indexed using a dictionary where keys represent attributes (e.g., genre, director, actor).
- Movies are scored based on matches:

    - +3 for genre
    - +2 for director
    - +1 for lead actor

- Results are sorted by scores and IMDb rating.
- Ideal for partial or flexible input searches.

## Technologies

- Python: Core programming language.
- Flask: Web framework for routing and templates.
- Pandas: Data handling and processing.
- HTML/CSS: Frontend for user interface.
