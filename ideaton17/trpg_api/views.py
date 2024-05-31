from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import openai
import json

# openai.api_key = ""

# 초기 스토리 설정
initial_story = """
당신은 판타지 세계의 모험가입니다. 당신의 여정은 작은 마을에서 시작됩니다. 마을 사람들은 도움을 필요로 하고, 당신에게 다양한 퀘스트를 제안합니다. 
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
        user_input = request.POST.get('input', '')

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
            max_tokens=150,
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
