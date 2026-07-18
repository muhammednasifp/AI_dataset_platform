from django.shortcuts import render
from django.http import HttpResponse
# from src.factories.rag_factory import RAGFactory
# from src.config import Config
from .services.dataset_service import DatasetService

def home(request):

    # config=Config()
    # factory_obj=RAGFactory(config=config)

    # rag_obj=factory_obj.factory()
    
    # answer=rag_obj.ask("What is Python")

    return render(request,'home/home.html')

def build_dataset(request):

    if request.POST:
        urls=request.POST.get('doc_urls')     
        chunk_size=request.POST.get('chunk_size') 
        top_k=request.POST.get('top_k')
        
        context=DatasetService.build(urls,chunk_size,top_k)

        return  render(request,'build_dataset/build_dataset.html',context)
    
    return  render(request,'build_dataset/build_dataset.html')


def chat_bot(request):
    return render(request,'chat_bot/chat_bot.html')