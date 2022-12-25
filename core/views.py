
from django.http import HttpResponse
import firebase_admin
from firebase_admin import credentials, firestore, messaging
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

cred = credentials.Certificate("mysite/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
users_ref = db.collection('shops')


def index(request):
    # accessing our firebase data and storing it in a variable
    docs = users_ref.stream()
    list = []
    for doc in docs:
        list.append(doc.to_dict())
    return HttpResponse(json.dumps(list))


@api_view(['POST'])
def sendNotification(request):
    print(request.data)
    try:
        # This registration token comes from the client FCM SDKs.
        registration_tokens = []
        transaction = request.data.get('transaction')
        print(transaction)
        tokens = request.data.get('tokens')
        for token in json.loads(tokens):
            registration_tokens.append(token)
            print(token)
        transaction_json = json.loads(transaction)

        # push trandaction data
        pending_transaction_ref = db.collection(u'pending_transactions')
        pending_document = pending_transaction_ref.document()
        pushTransactionData(pending_document ,transaction_json, request.data.get('shops'))

        # See documentation on defining a message payload.
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                'New rescue request', "More info"),
            tokens=registration_tokens
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send_multicast(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
        return Response(pending_document.id, status.HTTP_200_OK)
    except:
        return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)


def pushTransactionData(pending_document, transaction, shops):
    
    pending_document.set({
        u'id': pending_document.id,
        u'userId': transaction.get('userId'),
        u'userImage': transaction.get('userImage'),
        u'userFullName': transaction.get('userFullName'),
        u'userPhone': transaction.get('userPhone'),
        u'service': transaction.get('service'),
        u'startTime': transaction.get('startTime'),
        u'content': transaction.get('content'),
        u'userLocation': transaction.get('userLocation'),
        u'userFcmToken': transaction.get('userFcmToken'),
        u'shops': json.loads(shops),
    })
    current_transaction_ref = db.collection(u'current_transactions')
    current_transaction_ref.document(pending_document.id).set({
        u'id': pending_document.id,
        u'userId': transaction.get('userId'),
        u'userImage': transaction.get('userImage'),
        u'userFullName': transaction.get('userFullName'),
        u'userPhone': transaction.get('userPhone'),
        u'service': transaction.get('service'),
        u'startTime': transaction.get('startTime'),
        u'content': transaction.get('content'),
        u'userLocation': transaction.get('userLocation'),
        u'userFcmToken': transaction.get('userFcmToken'),
        u'shops': json.loads(shops),
    })


@api_view(['POST'])
def acceptShopNotification(request):
    try:
        # This registration token comes from the client FCM SDKs.
        fcmToken = request.data.get('token')

        # See documentation on defining a message payload.
        message = messaging.Message(
            notification=messaging.Notification(
                'Congratulations! Your shop is accepted.', "More info"),
            token = fcmToken
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
        return Response(status.HTTP_200_OK)
    except:
        return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def rejectShopNotification(request):
    try:
        # This registration token comes from the client FCM SDKs.
        fcmToken = request.data.get('token')

        # See documentation on defining a message payload.
        message = messaging.Message(
            notification=messaging.Notification(
                'Your shop is rejected', "More info"),
            token = fcmToken
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
        return Response(status.HTTP_200_OK)
    except:
        return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)