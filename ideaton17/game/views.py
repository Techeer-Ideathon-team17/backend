from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Player
import json

# 사용자 이름 입력 API
@csrf_exempt
def enter_name(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        request.session['name'] = name
        return JsonResponse({'message': 'Name received'}, status=200)
    return JsonResponse({'message': 'Invalid method'}, status=405)

# 종족 선택 API
@csrf_exempt
def choose_race(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        race = data.get('race')
        name = request.session.get('name')
        if name:
            Player.objects.create(name=name, race=race)
            return JsonResponse({'message': 'Player created successfully'}, status=200)
        return JsonResponse({'message': 'Name not found in session'}, status=400)
    return JsonResponse({'message': 'Invalid method'}, status=405)

# 모든 플레이어 정보를 반환하는 API 엔드포인트
def get_player(request):
    if request.method == 'GET':
        players = Player.objects.all().values('name', 'race')
        players_list = list(players)
        return JsonResponse(players_list, safe=False)
    return JsonResponse({'message': 'Invalid method'}, status=405)
