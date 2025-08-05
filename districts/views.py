from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def list_view(request):
    return render(request, 'districts.html')
