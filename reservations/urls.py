from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:slot_id>/', views.BookSlotView.as_view(), name='book_slot'),
]
