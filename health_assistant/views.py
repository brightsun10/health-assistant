# health_assistant/views.py

import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import ChatMessage
from .agent import HealthAgent

@login_required
def chat_view(request):
    """
    Renders the main chat page.
    """
    # Get the last 20 messages for this user to provide conversation history
    messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')[:20]
    return render(request, 'health_assistant/chat.html', {'messages': messages})

@login_required
@require_POST
@csrf_exempt # Note: In production, you should use proper CSRF handling with AJAX.
def process_message(request):
    """
    Processes an incoming message from the user via AJAX,
    gets a response from the agent, and returns it.
    """
    try:
        print("=== process_message called ===")
        print(request.body)
        data = json.loads(request.body)
        print(data)
        user_message = data.get('message')
        print(user_message)
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Build conversation history for the agent from the database
        # The Gemini API expects history in a specific format
        history = []
        past_messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp').values('message', 'response')
        for msg in past_messages:
            history.append({'role': 'user', 'parts': [{'text': msg['message']}]})
            history.append({'role': 'model', 'parts': [{'text': msg['response']}]})
        
        print(history)
        # Initialize and use the agent
        agent = HealthAgent(user=request.user)
        print(agent)
        bot_response = agent.get_response(user_message, history)
        
        
        print("Raw response from agent:", bot_response)
        print("Type:", type(bot_response))

        # Just in case it's not a string
        if not isinstance(bot_response, str):
                bot_response = str(bot_response)

        # Save the conversation to the database
        ChatMessage.objects.create(
            user=request.user,
            message=user_message,
            response=bot_response
        )

        return JsonResponse({'response': bot_response})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"ERROR OCCURRED: {e}")
        return JsonResponse({'error': str(e)}, status=500)
