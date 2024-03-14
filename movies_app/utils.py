def calculate_favorite_genres(collections):
    genre_counts = {}
    for collection in collections:
        for movie in collection.movies.all():
            genres = movie.genres.split(',')
            for genre in genres:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1

    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1],
                           reverse=True)
    favorite_genres = ', '.join([genre[0] for genre in sorted_genres[:3]])
    return favorite_genres
