from django.shortcuts import render
from django.http import HttpResponse
# from src.factories.rag_factory import RAGFactory
# from src.config import Config
def home(request):

    # config=Config()
    # factory_obj=RAGFactory(config=config)

    # rag_obj=factory_obj.factory()
    
    # answer=rag_obj.ask("What is Python")

    return render(request,'home/home.html')

def build_dataset(request):
   return  render(request,'build_dataset/build_dataset.html')

def chat_bot(request):
    return render(request,'chat_bot/chat_bot.html')