from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Municipality

@login_required(login_url='/')
def list_view(request, page_number=1):
    columns = ['api_id', 'name', 'state']

    filter_column = request.POST.get("filter-column")
    filter_value = request.POST.get("filter-value")

    if filter_column in columns and filter_value:
        if filter_column == 'state':
            municipalities = Municipality.objects.filter(**{f"{filter_column}__name__icontains": filter_value}).order_by('api_id')    
        else:
            municipalities = Municipality.objects.filter(**{f"{filter_column}__icontains": filter_value}).order_by('api_id')
        page_number = 1
    else:
        municipalities = Municipality.objects.all().order_by('api_id')

    paginator = Paginator(municipalities, 10)

    if page_number > paginator.num_pages:
        page_number = 1

    return render(request, 'municipalities.html', {
        'columns': columns, 
        'paginator': paginator.get_page(page_number),
        'first_page': 1,
        'current_page': page_number,
        'last_page': paginator.num_pages
        }
    )