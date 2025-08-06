from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Municipality

@login_required(login_url='/')
def list_view(request):
    columns = ['api_id', 'name', 'state']

    if request.method == 'POST':
        filter_column = request.POST.get("filter-column")
        filter_value = request.POST.get("filter-value")

        request.session["filter_column"] = request.POST.get("filter-column")
        request.session["filter_value"] = request.POST.get("filter-value")
        
        if filter_column and filter_value:
            request.session["filter_column"] = filter_column
            request.session["filter_value"] = filter_value
        else:
            request.session.pop("filter_column", None)
            request.session.pop("filter_value", None)

        page_number = 1
    else:
        try:
            page_number = int(request.GET.get("page", 1))
        except ValueError:
            page_number = 1

    filter_column = request.session.get("filter_column")
    filter_value = request.session.get("filter_value")

    if filter_column in columns and filter_value:
        if filter_column == 'state':
            municipalities = Municipality.objects.filter(**{f"{filter_column}__name__icontains": filter_value}).order_by('api_id')    
        else:
            municipalities = Municipality.objects.filter(**{f"{filter_column}__icontains": filter_value}).order_by('api_id')
    else:
        municipalities = Municipality.objects.all().order_by('api_id')

    paginator = Paginator(municipalities, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, 'municipalities.html', {
        'columns': columns, 
        'paginator': page_obj,
        'first_page': 1,
        'current_page': page_obj.number,
        'last_page': paginator.num_pages
        }
    )