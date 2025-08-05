from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import State

@login_required(login_url='/')
def list_view(request):
    states = State.objects.all()[:10]
    columns = ['apid_id', 'acronym', 'name']

    return render(request, 'states.html', {'data': states, 'columns': columns})
