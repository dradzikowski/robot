# Create your views here.
from collections import defaultdict

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
    # keywords = []
    # for keyword in requestBody['keywords']:
    #    keywords.append({'$or': [{"keyword": keyword}, {"keyword": keyword}]})
    # keywords.append({"keyword": {'$in': requestBody['keywords']}})
    # keywords.append({"keywords": {'$regex': '.*' + keyword + '.*'}})

    keywords = {"keyword": {'$in': requestBody['keywords']}}
    projection = {'keyword': 1, 'references': 1, '_id': 0}
    logging.warning(keywords)

    res = col.find(keywords, projection)

    # TODO indexes
    found_articles = intersect_articles(res)

    print found_articles

    articles = col.find({'article._id': {'$in': found_articles['references']}})#TODO poprawka
    # projection = {'url': 1, 'title': 1, 'art_date': 1, '_id': 0}

    print articles

    #print found_articles
        #print result  # zwracane {} i wywala sie
#        found.append({
#            "site": "techcrunch",
#            "url": result['url'],
#            "title": result['title'],
#            "art_date": result['art_date'],
#        })

    found = []
    data = dict() #defaultdict(list)#
    data['articles'] = found
    return JsonResponse(data)


def intersect_articles(res):
    last_result = None
    for result in res:
        current_result = result
        if last_result is not None and last_result != current_result:
            last_result = list(set(last_result['references']).intersection(current_result['references']))
        else:
            last_result = current_result
    return last_result


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
