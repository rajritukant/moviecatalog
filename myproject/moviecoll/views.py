from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Collection, Movie, Genre
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import moviecoll.config as app_config
import requests
import json
import time
# Create your views here.


def home(request):
    return HttpResponse('Credy movie collection assignment')


def home1(request):
    return HttpResponse('bbds')


class HelloView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {'message': 'Hello, Test passed. You are authenticated!!'}
        return Response(content)


class Movies(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            url = app_config.client_url
            username = app_config.client_id
            password = app_config.client_secret
            # retry strategy below max retries =5
            retry_strategy = Retry(
                total=5,
                status_forcelist=[429, 500, 502, 503, 504],
                method_whitelist=["HEAD", "GET", "OPTIONS"]
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            http = requests.Session()
            http.mount("https://", adapter)
            http.mount("http://", adapter)

            response = http.get(url, auth=(username, password))

            # response = requests.get(url, auth=(username, password))

            credy_api_response = json.loads(response.text)
            credy_api_response['my_message'] = 'getting movie list from credy'
            # because the problem statement says that response should have 'data'
            # so providing both 'data' and 'results'
            # knowing that This will increase size of response
            # TODO: use only one of them
            credy_api_response['data'] = credy_api_response['results']
            content = {'message': 'getting movie list from credy',
                       'credy_api_response': json.loads(response.text)}
            return Response(credy_api_response)
        except Exception as e:
            content = {'is_success': False,
                       'message': str(e)}
            return Response(content, status=status.HTTP_200_OK)

    def post(self, request):
        # dummy post request to make movie entries in db
        title = 'movie '+str(time.time() % 1000)
        desc = 'movie desc '+str(time.time() % 1000000)
        mov = Movie.objects.create(title=title, description=desc)
        return Response({'created_movie': mov.id}, status=status.HTTP_200_OK)


class UserCollection(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        # This should return my collection of movies and my top 3 favourite
        # genres based on the movies across all my collections.
        try:
            if request.user.is_authenticated:
                user = request.user
                username = user.username
            else:
                raise Exception('User not authenticated')
            response_data = {}
            # getting all collections for this user
            my_coll = Collection.objects.filter(user=user)
            print('my_coll')
            print(my_coll)
            coll_list = []
            for item in my_coll:
                temp_dict = {}
                temp_dict['id'] = item.id
                temp_dict['title'] = item.title
                temp_dict['description'] = item.description
                coll_list.append(temp_dict)

            # now getting top 3 genres using raw sql query
            query = """
                    SELECT gm.genre_id, g.name, count(*) as countg from moviecoll_genre_movie as gm 
INNER JOIN moviecoll_genre g ON gm.genre_id=g.id
where gm.movie_id in
(select DISTINCT(mc.movie_id) from moviecoll_movie_collection as mc
INNER JOIN moviecoll_collection ON mc.collection_id = moviecoll_collection.id
 where moviecoll_collection.user_id=1) GROUP BY gm.genre_id ORDER by countg desc limit 3;
            """
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                print(rows)
            top_3_genres = [item[1] for item in rows]

            response_data['collections'] = coll_list
            response_data['favourite_genres'] = top_3_genres
            response = {}
            response['is_success'] = True
            response['message'] = 'fetched collection for user: ' + username
            response['data'] = response_data
            # content = {'message': 'getting my collection'}
            return Response(response)
        except Exception as e:
            content = {'is_success': False,
                       'message': str(e)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # creates a collection for the user and returns id
        try:
            json_data = json.loads(str(request.body, encoding='utf-8'))
            if request.user.is_authenticated:
                user = request.user
            else:
                raise Exception('User not authenticated')
            title = json_data['title']
            description = json_data['description']
            coll = Collection.objects.create(
                title=title, description=description, user=user)
            # assuming that we get a list of movie ids and
            # movies with these ids are already in the db-table movies
            # adding entire movie list to collection in one shot
            movie_list = json_data['movies']
            # used * to expand list into arguments
            coll.movie_set.add(*movie_list)
            coll.save()
            response = {}
            response['collection_id'] = coll.id
            response['is_success'] = True
            response['message'] = 'created collection with id: ' + str(coll.id)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            content = {'is_success': False,
                       'message': str(e)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class ParticularCollection(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, id):
        # This should return title, description and list of movies in the collection
        try:
            coll = Collection.objects.get(id=id)
            response = {}
            response['is_success'] = True
            response['message'] = 'getting collection with id: '+str(id)
            response['title'] = coll.title
            response['description'] = coll.description
            # getting names of movies in the collection
            coll_movies = coll.movie_set.all()  # returns queryset
            movie_names = []
            for mov in coll_movies:
                movie_names.append(mov.title)
            response['movies'] = movie_names
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            content = {'is_success': False,
                       'message': 'no collection with given id: '+str(id)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        # This should delete the particular collection.
        print('her '*6)
        try:
            coll = Collection.objects.get(id=id).delete()
            print('fsadf '*6)
            content = {'is_success': True,
                       'message': 'deleted collection with id: '+str(id)}
            return Response(content, status=status.HTTP_200_OK)
        except Exception as e:
            content = {'is_success': False,
                       'message': 'no collection with given id: '+str(id)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        # This should update the particular collection. i.e. list of movies, title and description
        try:
            coll = Collection.objects.get(id=id)
            response = {}
            json_data = json.loads(str(request.body, encoding='utf-8'))
            if 'title' in json_data:
                coll.title = json_data['title']
            if 'description' in json_data:
                coll.description = json_data['description']
            if 'movies' in json_data:
                # updating(adding) list of movies in collection
                # assuming that we get a list of movie ids and
                # movies with these ids are already in the db-table movies

                # adding entire movie list to collection in one shot
                # used * to expand list into arguments
                coll.movie_set.add(*json_data['movies'])
                # iterating over movie list and adding one by one
                # for mov_id in json_data['movies']:
                #     # if movie already exists in our db then add it to collection otherwise create movie object and then add it to collection
                #     mov = Movie.objects.get(id=mov_id)
                #     mov.collections.add(coll)
                #     # or
                #     coll.movie_set.add(mov)
            coll.save()
            response['is_success'] = True
            response['message'] = 'updated collection with id: ' + str(id)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            content = {'is_success': False,
                       'message': 'no collection with given id: '+str(id)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class RequestCount(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        # 'number of requests served by this server till now'
        from .middleware import CounterMiddleware
        counter = CounterMiddleware.get_counter(self)
        content = {'requests': counter}
        return Response(content, status=status.HTTP_200_OK)


class RequestCountReset(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        # do something to reset the server request count
        from .middleware import CounterMiddleware
        counter = CounterMiddleware.reset_counter(self)
        content = {'message': 'request count reset successfully'}
        return Response(content, status=status.HTTP_200_OK)
