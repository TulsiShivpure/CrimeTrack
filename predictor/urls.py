from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),              # your index page
    path('predict/', views.predict, name='predict'),  # POST request handler
]
