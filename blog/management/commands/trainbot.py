from django.core.management import BaseCommand
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from .models import Conversation
from blog.views import bot  # Import your chatbot instance

class Command(BaseCommand):
    help = 'Train the chatbot'

    def handle(self, *args, **options):
        # Corpus training
        corpus_trainer = ChatterBotCorpusTrainer(bot)
        corpus_trainer.train('chatterbot.corpus.english')
        
        # Custom list training
        list_trainer = ListTrainer(bot)
        list_to_train = [
            "Hello!", "Hi there!",
            "How are you?", "I'm doing well, thank you!",
            "What is your name?", "I am a chatbot."
        ]
        list_trainer.train(list_to_train)
        
        self.stdout.write(self.style.SUCCESS('Successfully trained chatbot'))