from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from .models import Conversation
import json
import logging

logger = logging.getLogger(__name__)

# Initialize ChatBot
bot = ChatBot(
    'chatbot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///db.sqlite3',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90
        }
    ]
)

# Train only once
if not Conversation.objects.exists():  # Simple check to avoid retraining
    corpus_trainer = ChatterBotCorpusTrainer(bot)
    corpus_trainer.train('chatterbot.corpus.english')
    
    list_trainer = ListTrainer(bot)
    list_to_train = ["Hello!", "Hi there!", ...]  # Your custom list
    list_trainer.train(list_to_train)

@csrf_exempt
def getResponse(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('userMessage', '').strip()
            
            if not user_message:
                return JsonResponse({'response': 'Please type something!'})
            
            response = bot.get_response(user_message)
            chat_response = str(response) if response.confidence >= 0.5 else "I'm not sure."
            
            # Log and save
            logger.info(f"User: {user_message} | Bot: {chat_response}")
            Conversation.objects.create(
                user_message=user_message, 
                bot_response=chat_response
            )
            
            return JsonResponse({'response': chat_response})
        
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def index(request):
    return render(request, 'blog/index.html')