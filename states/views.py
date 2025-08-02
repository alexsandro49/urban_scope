from django.shortcuts import HttpResponse

def hello(request):
    return HttpResponse('Hellor World')
