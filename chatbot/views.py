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
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        body = json.loads(request.body)
        user_message = body.get("message", "").strip()

        if not user_message:
            return JsonResponse({"reply": "Please type something."})

        # Smart reply logic
        msg = user_message.lower()

        if any(word in msg for word in ["tutor", "lesson", "english", "math", "chemistry", "physics"]):
            bot_reply = "We offer private tutoring in English, Math, Chemistry, and more. Would you like to book a session?"
        elif any(word in msg for word in ["software", "app", "development", "programming", "website"]):
            bot_reply = "We build custom web, Android, and desktop software solutions. Tell us what you need built."
        elif any(word in msg for word in ["ict", "support", "troubleshooting", "network", "dhis2"]):
            bot_reply = "Our ICT services cover troubleshooting, training, networking, and DHIS2 support. What’s the issue?"
        elif any(word in msg for word in ["graphic", "design", "logo", "poster", "branding", "canva"]):
            bot_reply = "We design logos, posters, and branding materials. What kind of design do you need?"
        elif any(word in msg for word in ["marketing", "seo", "social", "campaign", "grow", "ads"]):
            bot_reply = "We help with SEO, social media, and marketing campaigns. What are you looking to promote?"
        elif any(word in msg for word in ["assistant", "pa", "schedule", "documents"]):
            bot_reply = "We offer virtual PA services for scheduling, task management, and more. Need help organizing?"
        elif any(word in msg for word in ["ai", "automation", "chatgpt", "bot", "jasper", "dalle"]):
            bot_reply = "Our AI services cover content generation, images, and task automation. How can we help?"
        elif any(word in msg for word in ["data", "excel", "python", "r", "dashboard", "survey", "research"]):
            bot_reply = "We analyze data using Excel, Python, R, Power BI, and more. Need data cleaning or visualization?"
        else:
            bot_reply = "I’m still learning about that! Try asking about tutoring, marketing, programming, design, or data work."

        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "apikey": SUPABASE_KEY,
        }

        # Prepare messages
        messages = [
            {"sender": "user", "text": user_message},
            {"sender": "bot", "text": bot_reply}
        ]

        # Send messages to Supabase
        for msg in messages:
            res = requests.post(
                f"{SUPABASE_URL}/rest/v1/chat_messages?apikey={SUPABASE_KEY}",
                headers=headers,
                json=msg
            )
            if res.status_code not in [200, 201]:
                print(f"❌ Error sending {msg['sender']} message: {res.text}")

        return JsonResponse({"reply": bot_reply})

    except Exception as e:
        print("Unhandled error:", str(e))
        return JsonResponse({"reply": "Oops! Something went wrong on our end."})
