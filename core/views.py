
from django.http import HttpResponse
import firebase_admin
from firebase_admin import credentials, firestore, messaging
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

@api_view(['POST'])
def sendNotification(request):
    # This registration token comes from the client FCM SDKs.
    registration_tokens = []
    for key in request.data:
        registration_tokens.append(key)
        print(key)

    # See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        notification=messaging.Notification('Price drop', '5% off all electronics'),
        tokens=registration_tokens,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    return Response()


def subscribe_news(tokens): # tokens is a list of registration tokens
 topic = 'news'
 response = messaging.subscribe_to_topic(tokens, topic)
 if response.failure_count > 0:
  print(f'Failed to subscribe to topic {topic} due to {list(map(lambda e: e.reason,response.errors))}')


def unsubscribe_news(tokens): # tokens is a list of registration tokens
 topic = 'news'
 response = messaging.unsubscribe_from_topic(tokens, topic)
 if response.failure_count > 0:
  print(f'Failed to unsubscribe to topic {topic} due to {list(map(lambda e: e.reason,response.errors))}')