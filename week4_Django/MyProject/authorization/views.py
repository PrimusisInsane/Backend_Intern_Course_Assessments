from django.shortcuts import render, redirect
from .models import Authorization

def index(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        joined_date = request.POST.get('joined_date')
        done = request.POST.get('done') =='true'
        phone = request.POST.get('phone number')
        if firstname and lastname:
            Authorization.objects.create(firstname=firstname, lastname=lastname, joined_date=joined_date, done=done)
        return redirect('index')

    authorization = Authorization.objects.all()
    return render(request, 'authorization/index.html', {'authorization': authorization})