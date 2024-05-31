from django.urls import path
from . import views

urlpatterns = [
    path('', views.trpg, name='trpg'),
]
