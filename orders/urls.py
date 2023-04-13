from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('track_order/', views.track_order, name='track_order'),
    path('order_complete/', views.order_complete, name='order_complete'),
]