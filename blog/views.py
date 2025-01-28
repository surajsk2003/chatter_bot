from django.shortcuts import render
from django.http import HttpResponse
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

bot = ChatBot('chatbot', read_only=False, logic_adapters= ['chatterbot.logic.BestMatch'])

list_to_train = [
    "hi",
    "hello",
    "i'm good",
    "That's good to hear",
    "Thank you",
    "You're welcome",
    "i am a chat bot",
    "That's nice",
    "what is your name",
    "my name is chatbot",
    "how are you",
    "I'm doing well",
    "What can you do?",
    "I can help you with chatbot",
]


lsit_trianer = ListTrainer(bot)

lsit_trianer.train(list_to_train)
def index(request):
    return render(request, 'blog/index.html')  # Ensure the template path is correct

def specific(request):
    return HttpResponse("list1")

def getResponse(request):
    userMessage = request.GET.get('userMessage')  # Get the user's message
    chatresponse = str(bot.get_response(userMessage))
    return HttpResponse(chatresponse)  # Return the bot's response
