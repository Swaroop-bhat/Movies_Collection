import requests
from django.conf import settings


def fetch_movies():
    url = 'https://demo.credy.in/api/v1/maya/movies/'
    response = requests.get(url)
    print("response is", response)
    if response.status_code == 200:
        data = response.json()
        count = data.get('count', 0)
        next_page = data.get('next')
        previous_page = data.get('previous')
        movies = data.get('results', [])
        return {
            'count': count,
            'next': next_page,
            'previous': previous_page,
            'movies': movies
        }
    else:
        return {
            'count': 0,
            'next': None,
            'previous': None,
            'movies': []
        }


def calculate_favorite_genres(collections):
    genre_counts = {}
    for collection in collections:
        for movie in collection.movies.all():
            genres = movie.genres.split(',')
            for genre in genres:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1

    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
    favorite_genres = ', '.join([genre[0] for genre in sorted_genres[:3]])
    return favorite_genres