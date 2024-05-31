from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import openai
import json



# 초기 스토리 설정
initial_story = """
"""

# 사용자의 이전 대화 상태를 저장할 수 있도록 구성
session_data = {
    "story": initial_story,
    "history": []
}


@csrf_exempt
def trpg(request):
    response_text = None

    if request.method == 'POST':
        json_data = json.loads(request.body)
        # 'text' 필드 값 가져오기
        user_input = json_data.get('user_input')
        if 'count' not in request.session:
            request.session['count'] = 0
        elif request.session['count'] >= 5:
            response_text = "게임이 종료 되었습니다."
            return JsonResponse({'response_text': response_text})
        count = request.session['count']
        request.session['count'] += 1
        print(user_input)
        print(count)
        if count == 0:
            user_input = f"플레이어의 이름은: {user_input}이야 이제 직업을 직업을 물어봐줄래?"

        elif count == 1:
            user_input = f"플레이어의 직업은:{user_input}이야. 판타지 세계의 모험가입니다. 당신의 여정은 작은 마을에서 시작됩니다. 마을 사람들은 도움을 필요로 하고, 당신에게 3지선다의 다양한 퀘스트를 제안합니다. 모든 제안은 3지선다 입니다."

        # 이전 대화 기록과 새로운 입력을 결합하여 프롬프트 생성
        prompt = f"{session_data['story']}\n\n"
        for h in session_data["history"]:
            prompt += f"Player: {h['input']}\n"
            prompt += f"Game Master: {h['response']}\n"
        prompt += f"Player: {user_input}\nGame Master:"

        # GPT-4 호출
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.9,
        )

        # 모델의 응답 추출
        gpt_response = response['choices'][0]['message']['content'].strip()

        # 대화 기록 업데이트
        session_data["history"].append({
            "input": user_input,
            "response": gpt_response
        })

        # 이야기 업데이트
        session_data["story"] += f"\nPlayer: {user_input}\nGame Master: {gpt_response}"

        response_text = gpt_response

    # return render(request, 'trpg_api/index.html', {'response': response_text})
    return JsonResponse({'response_text': response_text}, safe=False)
