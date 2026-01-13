from . import views
from django.urls import path

app_name = 'BBMS'
urlpatterns = [
  path('', views.index,name='index'),
 
]
