import os
import requests
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@csrf_exempt
def chatbot_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    try:
        body = json.loads(request.body)
        user_message = body.get("message", "").strip()

        if not user_message:
            return JsonResponse({"reply": "Please type something."})

        # === Simple local logic ===
        # Later, replace this with Dialogflow or GPT API
        if "tutor" in user_message.lower():
            bot_reply = "We offer expert private tutoring in a range of subjects. What level or topic are you interested in?"
        elif "marketing" in user_message.lower():
            bot_reply = "We can help with digital marketing, content, SEO, and more. Want to chat with our marketing team?"
        elif "programming" in user_message.lower():
            bot_reply = "We provide full-stack and custom software solutions. What kind of project do you have in mind?"
        elif "ict" in user_message.lower():
            bot_reply = "Our ICT services include support, training, and systems setup. What are you looking for?"
        elif "data" in user_message.lower():
            bot_reply = "We analyze and visualize data for businesses, research, and more. Would you like to schedule a consultation?"
        elif "personal assistant" in user_message.lower() or "pa" in user_message.lower():
            bot_reply = "Our personal assistant services cover scheduling, email management, and more. Need help managing your day?"
        else:
            bot_reply = f"You said: {user_message}"

        # === Save user + bot messages to Supabase ===
        supabase_messages = [
            {"sender": "user", "text": user_message},
            {"sender": "bot", "text": bot_reply}
        ]

        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }

        res = requests.post(
            f"{SUPABASE_URL}/rest/v1/chat_messages",
            headers=headers,
            json=supabase_messages
        )

        if res.status_code not in [200, 201]:
            print("Supabase error:", res.text)

        return JsonResponse({"reply": bot_reply})

    except Exception as e:
        print("Backend error:", str(e))
        return JsonResponse({"reply": "Oops! Something went wrong on our end."}, status=500)
