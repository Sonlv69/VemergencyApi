
from django.http import HttpResponse
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

cred = credentials.Certificate("mysite/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
users_ref = db.collection('shop_clones')



def index(request):
        #accessing our firebase data and storing it in a variable
        docs = users_ref.stream()
        list = []
        for doc in docs:
            list.append(doc.to_dict())

        return HttpResponse(json.dumps(list))