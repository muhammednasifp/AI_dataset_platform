from django.shortcuts import render
from django.http import HttpResponse
# from src.factories.rag_factory import RAGFactory
# from src.config import Config
from .services.dataset_service import DatasetService
from .services.chat_service import ChatService
from .services.analytics_service import AnalyticsService
def home(request):

    return render(request,'home/home.html')

def build_dataset(request):

    if request.method=="POST":
        
        urls=request.POST.get('doc_urls')     
        chunk_size=request.POST.get('chunk_size') 
        top_k=request.POST.get('top_k')
        
        context=DatasetService.build(urls,chunk_size,top_k)

        return  render(request,'build_dataset/build_dataset.html',context)
    
    return  render(request,'build_dataset/build_dataset.html')


def chat_bot(request):

    if request.method == "POST":
        question=request.POST.get('question') 

        context=ChatService.ask(question=question)

        context["question"]=question

        return render(request,'chat_bot/chat_bot.html',context)
        
    return render(request,'chat_bot/chat_bot.html')

def analytics(request):

    context=AnalyticsService.get_statics()

    print(context["low_quality_doc_count"])
    
    return render(request,'analytics/analytics.html',context)
