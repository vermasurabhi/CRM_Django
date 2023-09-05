from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
## for login and logout messages
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()
    # check to see if logging in
    if request.method=="POST":
        username = request.POST['username'] #username inside the POST is the name inside the input tag of home.html
        password = request.POST['password'] #password inside the POST is the name inside the input tag of home.html
        # Authenticate
        user = authenticate(request, username=username, password= password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged In!")
            return redirect('home')
        else:
            messages.success(request, "There was an error Loggin In, Please try again")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged out...")
    return redirect('home')

def register_user(request):
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have Successfully Registered!")
            return redirect('home')
    else:
        form = SignUpForm()  #we are not posting the request here this else is just for the displaying of registration form which will definetely take the SignUpForm class for the registration form style displaying
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up records
        customer_record = Record.objects.get(id=pk) #instead of using all we just mentioned get to open that specfic id
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You must be logged in to view that page!")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted successfully!")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to view that page!")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added..")
                return redirect('home')        
        return render(request, 'add_record.html', {'form': form}) 
    else:
        messages.success(request, "You must be logged in to view that page!")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated")
            return redirect('home')   
        return render(request, 'update_record.html', {'form': form}) 
    else:
        messages.success(request, "You must be logged in to view that page!")
        return redirect('home')
