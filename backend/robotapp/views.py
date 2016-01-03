# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from rest_framework.decorators import api_view
import logging
import json
from robotapp.db import MongoDBClient


@api_view(["GET"])
@csrf_exempt
def index(request):
    return render_to_response('index.html')


@api_view(["POST"])
@csrf_exempt
def findByKeywords(request):
    col = MongoDBClient('techcrunch').collection

    requestBody = json.loads(request.body)

    # todo: add strategies - exact match and regex match;
    # todo: case insensitive
    keywords = []
    for keyword in requestBody['keywords']:
        keywords.append({"keywords": {'$regex': '.*' + keyword + '.*'}})

    # temp
    logging.warning(keywords)

    projection = {'url': 1, 'title': 1, 'art_date': 1, '_id': 0}

    res = col.find({"$and": keywords}, projection)

    found = []
    for result in res:
        found.append({
            "site":"techcrunch",
            "url": result['url'],
            "title": result['title'],
            "art_date": result['art_date'],
        })

    data = dict()
    data['articles'] = found
    return JsonResponse(data)


# NOT USED
@api_view(["POST"])
@csrf_exempt
def insert(request):
    uri = "mongodb://admin:admin@ds061454.mongolab.com:61454/robot"
    client = MongoClient(uri)
    db = client['robot']
    col = db.crawled
    res = col.insert_one({"name": request.POST['name']})
    name = request.POST['name']
    return render_to_response('home.html', locals())
