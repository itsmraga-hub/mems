from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def homeview(request):
  # return HttpResponse('index.html')
  return render(request, 'index.html')


def admin_dashboard(request):
  return render(request, 'admin_dashboard.html')