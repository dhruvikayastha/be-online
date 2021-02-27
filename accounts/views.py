from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

def register(request):

    if request.method == 'POST':
        #get form value
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #check if passwors match
        if password == password2:
            #check user name
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That User Name Is Taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email Is Already Registered')
                    return redirect('register')
                else:
                    #creating user
                    user = User.objects.create_user(username=username, password=password, email=email, first_name= first_name, last_name=last_name)
                    user.save()
                    messages.success(request, 'You Are Now Registered And Can Login ')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords Do Not Match')
            return redirect('register')
        return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        #get form value
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You Are Now Logged In')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Logged Out Successfully')
        return redirect('index')
