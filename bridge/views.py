# bridge/views.py

import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@csrf_exempt  # Exempt from CSRF for API access
def send_message(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            message = data.get('message')
            sender = data.get('sender', 'Unknown Sender')  # Default value if sender not provided

            if not message:
                return JsonResponse({'error': 'Message field is required.'}, status=400)

            # Forward the message to Telegram
            telegram_response = forward_to_telegram(message, sender)

            if telegram_response:
                return JsonResponse({'status': 'Message sent to Telegram successfully.'}, status=200)
            else:
                return JsonResponse({'error': 'Failed to send message to Telegram.'}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            # Return the exact exception message for debugging purposes
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)


def forward_to_telegram(message, sender):
    telegram_api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    full_message = f"New Message from {sender}:\n\n{message}"
    payload = {
        'chat_id': settings.TELEGRAM_CHAT_ID,
        'text': full_message
    }
    try:
        response = requests.post(telegram_api_url, json=payload)
        if response.status_code == 200:
            logger.info('Message successfully sent to Telegram.')
            return True
        else:
            # Log detailed error with status code and response
            logger.error(f"Failed to send message to Telegram: Status {response.status_code}, Response {response.text}")
            return False
    except Exception as e:
        # Log any exceptions that occur during the request
        logger.error(f"Error sending message to Telegram: {e}")
        return False
