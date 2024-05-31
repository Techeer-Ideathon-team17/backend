from django.shortcuts import render, redirect
from django.http import JsonResponse
from models import Player

# 시작 페이지 렌더링
def start(request):
    return render(request, 'game/start.html')

# 사용자 이름 입력 페이지 처리
def enter_name(request):
    if request.method == 'GET':
        return render(request, 'game/enter_name.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        request.session['name'] = name
        return redirect('choose_race')

# 종족 선택 페이지 처리
def choose_race(request):
    if request.method == 'GET':
        return render(request, 'game/choose_race.html')
    elif request.method == 'POST':
        race = request.POST.get('race')
        name = request.session.get('name')
        if name:
            Player.objects.create(name=name, race=race)
            return JsonResponse({'message': 'Player created successfully'})
        else:
            return JsonResponse({'message': 'Name not found in session'}, status=400)

# 모든 플레이어 정보를 반환하는 API 엔드포인트
def get_player(request):
    if request.method == 'GET':
        players = Player.objects.all().values('name', 'race')
        players_list = list(players)
        return JsonResponse(players_list, safe=False)
