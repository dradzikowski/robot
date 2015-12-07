# Create your views here.

from django.shortcuts import render_to_response
from pymongo import MongoClient

def home(request):
    client = MongoClient('localhost', 27017)
    db = client['test']
    col = db.restaurants
    res = col.find_one({"name":"Daniel"})
    name = str(res['name'])
    id = str(res['_id'])
    return render_to_response('home.html', locals())