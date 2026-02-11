from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from groq import Groq

# HOME PAGE
def home(request):
    return render(request, 'index.html')

# AI CONSULTATION - NO LOGIN REQUIRED, NO DATABASE
@csrf_exempt
def consultation(request):
    if request.method == 'POST':
        symptoms = request.POST.get('symptoms', '')
        try:
            client = Groq(api_key=os.environ.get('GROQ_API_KEY', ''))
            chat_completion = client.chat.completions.create(
                messages=[{
                    "role": "system",
                    "content": "You are Dr. R (Muganga Wange), a medical AI assistant for Rwanda. Ask one follow-up question about symptoms. Never diagnose. Suggest seeing a doctor for serious cases. Respond in English or Kinyarwanda."
                }, {
                    "role": "user",
                    "content": f"Patient symptoms: {symptoms}"
                }],
                model="llama-3.1-8b-instant",
            )
            ai_response = chat_completion.choices[0].message.content
            return render(request, 'result.html', {
                'symptoms': symptoms,
                'ai_response': ai_response
            })
        except Exception as e:
            return render(request, 'consultation.html', {'error': str(e)})
    return render(request, 'consultation.html')

urlpatterns = [
    path('', home, name='home'),
    path('consult/', consultation, name='consultation'),
    path('admin/', admin.site.urls),
]
