# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from rest_framework.decorators import api_view


@api_view(["GET"])
@csrf_exempt
def index(request):
    return render_to_response('index.html')

@api_view(["POST"])
@csrf_exempt
def find(request):
    uri = "mongodb://admin:admin@ds061454.mongolab.com:61454/robot"
    client = MongoClient(uri)
    db = client['robot']
    col = db['techcrunch']
    res = col.find({request.POST['key']:request.POST['value']}, {'url': 1, '_id': 0})
    #--------------------request.POST['key']:request.POST['value']
    #db.student.find({}, {roll:1, _id:0})
    #res = html_decode(str(res))
    found = []
    for result in res:
        found.append(result['url'])
    res = found
    data = dict()
    data['urls'] = res
    res = data
    #res = str(html_decode(str(found)))
    #name = request.POST['name']
    #res = json.loads(str(res))
    return JsonResponse(res)
    #return render_to_response('home.html', locals())

@api_view(["POST"])
@csrf_exempt
def insert(request):
    uri = "mongodb://admin:admin@ds061454.mongolab.com:61454/robot"
    client = MongoClient(uri)
    db = client['robot']
    col = db.crawled
    res = col.insert_one({"name":request.POST['name']})
    name = request.POST['name']
    return render_to_response('home.html', locals())

def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s