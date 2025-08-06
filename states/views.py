from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import State

@login_required(login_url='/')
def list_view(request, page_number=1):
    columns = ['api_id', 'acronym', 'name']

    filter_column = request.POST.get("filter-column")
    filter_value = request.POST.get("filter-value")

    if filter_column in columns and filter_value:
        states = State.objects.filter(**{f"{filter_column}__icontains": filter_value}).order_by('api_id')
    else:
        states = State.objects.all().order_by('api_id')

    paginator = Paginator(states, 10)

    if page_number > paginator.num_pages:
        page_number = 1

    return render(request, 'states.html', {
        'data': states, 'columns': columns, 
        'paginator': paginator.get_page(page_number),
        'first_page': 1,
        'current_page': page_number,
        'last_page': paginator.num_pages
        }
    )