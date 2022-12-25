from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('noti', views.sendNotification, name='send-rescue-notification'),
    path('acceptShopNoti', views.acceptShopNotification, name='send-accept-shop-notification'),
    path('rejectShopNoti', views.rejectShopNotification, name='send-reject-shop-notification'),
    path('createShopNoti', views.createShopNotification, name='create-shop-notification'),
]
