# Create your views here.

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient

@csrf_exempt
def find(request):
    client = MongoClient('localhost', 27017)
    db = client['test']
    col = db.restaurants
    res = col.find_one({"name":request.POST['name']})
    name = request.POST['name']
    return render_to_response('home.html', locals())

@csrf_exempt
def insert(request):
    client = MongoClient('localhost', 27017)
    db = client['test']
    col = db.restaurants
    res = col.insert_one({"name":request.POST['name']})
    name = request.POST['name']
    return render_to_response('home.html', locals())