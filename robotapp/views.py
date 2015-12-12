# Create your views here.

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient

@csrf_exempt
def find(request):
    uri = "mongodb://admin:admin@ds061454.mongolab.com:61454/robot"
    client = MongoClient(uri)
    db = client['robot']
    col = db.crawled
    res = col.find_one({"name":request.POST['name']})
    name = request.POST['name']
    return render_to_response('home.html', locals())

@csrf_exempt
def insert(request):
    uri = "mongodb://admin:admin@ds061454.mongolab.com:61454/robot"
    client = MongoClient(uri)
    db = client['robot']
    col = db.crawled
    res = col.insert_one({"name":request.POST['name']})
    name = request.POST['name']
    return render_to_response('home.html', locals())