from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Collection, Movie, User
from .auth import generate_jwt_token, verify_jwt_token
from .utils import fetch_movies, calculate_favorite_genres
from movies_collection import settings
from .serializers import MovieSerializer


@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password are required'},
                        status=status.HTTP_400_BAD_REQUEST)
    hashed_password = make_password(password)
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'password': hashed_password})
    if not created:
        return Response({'error': 'Username already exists'},
                        status=status.HTTP_400_BAD_REQUEST)

    token = generate_jwt_token(user.id)
    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'jwt': token
    }
    return response


import requests
@api_view(['GET'])
# def list_movies(request):
#     if request.method == 'GET':
#         authorization = request.headers.get('Authorization')
#         token = request.COOKIES.get('jwt')
#         payload = verify_jwt_token(token)
#         if not payload or not authorization:
#             return Response({'error': 'Unauthorized'},
#                             status=status.HTTP_401_UNAUTHORIZED)
            
#         movies_data = fetch_movies()
#         return Response(movies_data)

def list_movies(request):
    url = 'https://demo.credy.in/api/v1/maya/movies/'
    username = settings.MOVIE_API_USERNAME
    password = settings.MOVIE_API_PASSWORD
    print(username)
    # print(MOVIE_API_PASSWORD)
    
    username = 'iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0'
    password = 'Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1'

    retries = 3
    for _ in range(retries):
        try:
            response = requests.get(url, auth=(username, password))
            response.raise_for_status()
            data = response.json()
            return Response(data, status=response.status_code)
        except requests.RequestException as e:
            print(f"Error fetching movies: {e}")
    return Response({'error': 'Failed to fetch movies'}, status=500)

    

@api_view(['GET', 'POST'])
def list_create_collections(request):
    if request.method == 'GET':
        authorization = request.headers.get('Authorization')
        token = request.COOKIES.get('jwt')
        payload = verify_jwt_token(token)
        if not payload or not authorization:
            return Response({'error': 'Unauthorized'},
                            status=status.HTTP_401_UNAUTHORIZED)

        collections = Collection.objects.filter(
            user_id=payload['user_id'])
        data = [{'title': collection.title,
                 'uuid': collection.uuid,
                 'description': collection.description
                 } for collection in collections]
        favorite_genres = calculate_favorite_genres(collections)

        return Response({
            'is_success': True,
            'data': {
                'collections': data,
                'favorite_genres': favorite_genres
            }
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        authorization = request.headers.get('Authorization')
        token = request.COOKIES.get('jwt')
        payload = verify_jwt_token(token)
        if not payload or not authorization:
            return Response({'error': 'Unauthorized'},
                            status=status.HTTP_401_UNAUTHORIZED)

        title = request.data.get('title')
        description = request.data.get('description')
        movies = request.data.get('movies')

        if not title or not movies:
            return Response({'error': 'Title and movies are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        collection = Collection.objects.create(
            title=title, description=description,
            user_id=payload['user_id'])
        for movie_data in movies:
            movie = Movie.objects.create(**movie_data)
            collection.movies.add(movie)

        return Response({'collection_uuid': collection.uuid},
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def retrieve_update_delete_collection(request, collection_uuid):
    authorization = request.headers.get('Authorization')
    token = request.COOKIES.get('jwt')
    payload = verify_jwt_token(token)
    if not payload or not authorization:
        return Response({'error': 'Unauthorized'},
                        status=status.HTTP_401_UNAUTHORIZED)

    collection = get_object_or_404(Collection,
                                   uuid=collection_uuid,
                                   user_id=payload['user_id'])

    if request.method == 'GET':
        data = {
            'title': collection.title,
            'description': collection.description,
            'movies': [{'title': movie.title,
                        'description': movie.description,
                        'genres': movie.genres,
                        'uuid': movie.uuid
                        } for movie in collection.movies.all()]
        }
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        movie_serializer = MovieSerializer(data=request.data)
        if movie_serializer.is_valid():
            movie = movie_serializer.save()
            collection.movies.add(movie)
            return Response({"status":
                "Movie added to collection successfully."},
                            status=status.HTTP_201_CREATED)
        return Response(movie_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        title = request.data.get('title')
        description = request.data.get('description')
        movies = request.data.get('movies')

        if title:
            collection.title = title
        if description:
            collection.description = description
        if movies:
            collection.movies.clear()
            for movie_data in movies:
                existing_movie = Movie.objects.filter(
                    title=movie_data['title'],
                    uuid=movie_data['uuid']).first()
                if existing_movie:
                    collection.movies.add(existing_movie)
                else:
                    movie = Movie.objects.create(**movie_data)
                    collection.movies.add(movie)

            collection.save()
            return Response({"status": "Collection updated successfully."},
                            status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            collection.delete()
            return Response({"status": "Collection deleted successfully."},
                            status=status.HTTP_204_NO_CONTENT)


def request_count(request):
    # return JsonResponse({'requests': settings.REQUEST_COUNT})
    count = getattr(request, 'request_count', 0)
    return JsonResponse({'request_count': count})


def reset_request_count(request):
    settings.REQUEST_COUNT = 0
    return JsonResponse({'message': 'Request count reset successfully'})
