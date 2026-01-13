# meeting_app/urls.py
from django.urls import path 
from . import views

urlpatterns = [
   path('', views.calendar_view, name='calendar_view'),
   path('time-slots/', views.get_time_slots, name='get_time_slots'),
   path('book-slot/<int:slot_id>/', views.book_time_slot, name='book_time_slot'),
   path('create-booking/', views.create_booking_view, name='create_booking'),
         
   
]