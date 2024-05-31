from django.urls import path
from . import views

urlpatterns = [
    path('enter_name/', views.enter_name, name='enter_name'),
    path('choose_race/', views.choose_race, name='choose_race'),
    path('api/players/', views.get_player, name='get_player'),  # API 엔드포인트 추가
]
