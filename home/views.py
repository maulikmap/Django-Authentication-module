from re import template
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from accounts.models import CustomUser


def index(request):
    context = {}
    
    uid = request.session.get("uid")
    
    user = CustomUser.objects.filter(id=uid).first()
    
    if user is not None:
        context["user"] = user
    
    return render(request, 'home.html', context=context)