from os import name

from django.shortcuts import render, redirect
from .models import Authorization

def index(request):
    authorization = Authorization.objects.all()
    return render(request, 'authorization/index.html', {'authorization': authorization})

def add(request):
    if request.method == 'POST':
       firstname = request.POST.get('firstname')
       lastname = request.POST.get('lastname')
       joined_date = request.POST.get('joined_date')
       done = request.POST.get('done') == 'true'
       phone = request.POST.get('phone number')
        
       if firstname and lastname:
            Authorization.objects.create(firstname=firstname, lastname=lastname, joined_date=joined_date, done=done, phone=phone)
       return redirect('authorization')
    return render(request, 'authorization/add.html')
