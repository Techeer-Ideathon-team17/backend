from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_start_page, name='render_start_page'),
    path('start/', views.start_chat, name='start_chat'),
    path('trpg/', views.trpg, name='trpg'),
]
