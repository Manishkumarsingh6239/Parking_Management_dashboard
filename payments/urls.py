from django.urls import path
from . import views

urlpatterns = [
    path('<int:reservation_id>/', views.payment_page, name='payment'),
    path('success/<int:payment_id>/', views.payment_success, name='payment_success'),
]
