# Create your views here.
from collections import defaultdict
from bson import ObjectId
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from rest_framework.decorators import api_view
import logging
import json
from robotapp.db import MongoDBClient
from robotapp.db import MongoDBNoCollectionClient


@api_view(["GET"])
@csrf_exempt
def index(request):
    return render_to_response('index.html')


@api_view(["POST"])
@csrf_exempt
def findByKeywords(request):
    db = MongoDBNoCollectionClient()
    articles_collection = db.client['articles']
    keywords_collection = db.client['keywords']

    requestBody = json.loads(request.body)

    # todo: add strategies - exact match and regex match;
    # todo: case insensitive
    # keywords = []
    # for keyword in requestBody['keywords']:
    #    keywords.append({'$or': [{"keyword": keyword}, {"keyword": keyword}]})
    # keywords.append({"keyword": {'$in': requestBody['keywords']}})
    # keywords.append({"keywords": {'$regex': '.*' + keyword + '.*'}})



    keywords = {"keyword": {'$in': [keyword.lower() for keyword in requestBody['keywords']]}}
    projection = {'keyword': 1, 'references': 1, '_id': 0}
    logging.warning(keywords)

    res = keywords_collection.find(keywords, projection)

    # logging.warning("Before intersection:")
    # for r in res:
    #    logging.warning(r)

    keywords_count = len(requestBody['keywords'])
    # TODO indexes!!!!!!!!!!!!!
    found_articles = intersect_articles(res, keywords_count)
    logging.warning("After intersection:")
    logging.warning(found_articles)

    objectIds = []
    if found_articles is not None:
        for found_article in found_articles:  # gdy jedno znalezione,a drugie nie, zwraca normalnie jedno slowo, bez intersekcji
            objectIds.append(ObjectId(found_article))

    articles = articles_collection.find({'_id': {'$in': objectIds}})
    # projection = {'url': 1, 'title': 1, 'art_date': 1, '_id': 0}

    # logging.warning("ARTICLES FOUND")

    data = defaultdict(list)

    for article in articles:
        article['_id'] = str(article['_id'])
        data['articles'].append(article)
        # logging.warning(article)


        # print result  # zwracane {} i wywala sie
    #        found.append({
    #            "site": "techcrunch",
    #            "url": result['url'],
    #            "title": result['title'],
    #            "art_date": result['art_date'],
    #        })

    return JsonResponse(data)


# chyba cos popsulem - liczba artykulow vs liczba stron z artykulami, a moze i nie?
def intersect_articles(res, keywords_count):
    if res.count() != keywords_count:
        logging.warning("No results found for at least one of the keywords")
        return []
    if keywords_count == 1:
        logging.warning("Searched for only one keyword, intersection does not occur")
        return res[0]['references']

    logging.warning("Starting intersection...")
    last_result = None
    for result in res:
        logging.warning(result)
        current_result = result
        logging.warning('Processed result:')
        logging.warning(current_result)
        if last_result is not None and last_result != current_result:
            last_result['references'] = list(set(last_result['references']).intersection(current_result['references']))
            # last_result = list(set(last_result['references']).intersection(current_result['references']))
            # bo juz nie ma references? moze wycofac te zmieny?
        else:
            last_result = current_result
    logging.warning("Ending intersection...")
    return last_result['references']


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
