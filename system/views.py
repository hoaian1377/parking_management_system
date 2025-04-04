from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')
def login(request):
    return render(request,'login.html')
def register(request):
    return render(request,'register.html')
def vehicle_management(request):
    return render(request,'vehicle_management.html')
def parking_status(request):
    return render(request,'parking_status.html')
def vehicle_report(request):
    return render(request, 'vehicle_report.html')


