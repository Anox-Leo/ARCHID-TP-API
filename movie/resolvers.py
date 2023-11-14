import json

def movie_with_id(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

def update_movie_rate(_,info,_id,_rating):
    new_movies = {}
    new_movie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rating
                new_movie = movie
                new_movies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(new_movies, wfile)
    return new_movie

def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        return actors

def movie_with_title(_,info,_title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == _title:
                return movie

def create_new_movie(_,info,_id,_rating,_title,_director):
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        new_movies = json.load(rfile)
        new_movie = {
            "id": _id,
            "rating": _rating,
            "title": _title,
            "director": _director
        }
        new_movies["movies"].append(new_movie)
        with open('{}/data/movies.json'.format("."), "w") as wfile:
            json.dump(new_movies, wfile)
        return new_movie

def delete_movie(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        new_movies = []
        deleted_movie = {}
        for movie in movies["movies"]:
            if movie['id'] != _id:
                new_movies.append(movie)
            else:
                deleted_movie = movie
        if deleted_movie:
            with open('{}/data/movies.json'.format("."), "w") as wfile:
                json.dump({
                    "movies": new_movies
                }, wfile)
        return deleted_movie
