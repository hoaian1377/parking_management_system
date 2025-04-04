from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')
def login(request):
    return render(request,'login.html')
def register(request):
    return render(request,'register.html')
def vehicle_entry(request):
    return render(request,'vehicle_entry.html')
def parking_status(request):
    return render(request,'parking_status.html')
