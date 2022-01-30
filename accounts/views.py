from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls.conf import path

# Create your views here.

def login(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']

        # Form authentication
        if username == '':
            messages.error(request, 'Username cannot be empty')
            return redirect('login')
        elif password == '':
            messages.error(request, 'password field cannot be empty')
        else:
            # User authentication
            user = auth.authenticate(
                username = username,
                password = password
            )

            if user is None:
                messages.error(request, 'Invalid login credentials')
                return redirect('login')
            else:
                auth.login(request, user)
                return redirect('home:manage_items')

    else:    
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        data = request.POST
        fname = data['fname']
        lname = data['lname']
        username = data['username']
        email = data['email']
        password1 = data['password']
        password2 = data['confirm_password']

        # Form Validation
        if fname == '':
            messages.error(request, 'First name cannot be empty')
            return redirect('register')
        elif lname == '':
            messages.error(request, "Last name cannot be emoty")
            return redirect('register')
        elif username == '':
            messages.error(request, 'Username cannot be empty')
            return redirect('register')
        elif email == '':
            messages.error(request, 'email field cannot be empty')
            return redirect('register')
        elif password1 != password2:
            messages.error(request, 'passwords do not match')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exist')
            return redirect('regster')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Already registered an account with this email')
            return redirect('register')
        else:

            user = User.objects.create(
                username=username, 
                password=password1, 
                email=email, 
                first_name=fname, 
                last_name=lname
            )

            # Authenticate and log user in
            auth.login(request, user)
            return redirect('home:manage_items')
            
    else:
        return render(request, 'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


# user login 
def login_user(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']

        # Form authentication
        if username == '':
            messages.error(request, 'Username cannot be empty')
            return redirect('login')
        elif password == '':
            messages.error(request, 'password field cannot be empty')
        else:
            # User authentication
            user = auth.authenticate(
                username = username,
                password = password
            )

            if user is None:
                messages.error(request, 'Invalid login credentials')
                return redirect('login_user')
            else:
                auth.login(request, user)
                return redirect('products:products')

    else:    
        return render(request, 'user_login.html')

# user registration
def reg_user(request):
    if request.method == 'POST':
        data = request.POST
        fname = data['fname']
        lname = data['lname']
        username = data['username']
        email = data['email']
        password1 = data['password']
        password2 = data['confirm_password']

        # Form Validation
        if fname == '':
            messages.error(request, 'First name cannot be empty')
            return redirect('reg_user')
        elif lname == '':
            messages.error(request, "Last name cannot be emoty")
            return redirect('reg_user')
        elif username == '':
            messages.error(request, 'Username cannot be empty')
            return redirect('reg_user')
        elif email == '':
            messages.error(request, 'email field cannot be empty')
            return redirect('reg_user')
        elif password1 != password2:
            messages.error(request, 'passwords do not match')
            return redirect('reg_user')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exist')
            return redirect('reg_user')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Already registered an account with this email')
            return redirect('reg_user')
        else:

            user = User.objects.create(
                username=username, 
                password=password1, 
                email=email, 
                first_name=fname, 
                last_name=lname,
                is_staff=True
            )

            # Authenticate and log user in
            auth.login(request, user)
            return redirect('products:products')
            
    else:
        return render(request, 'user_reg.html')