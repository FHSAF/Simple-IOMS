from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
# from contacts.models import Contact
from accounts import models
import re

from accounts.forms import EditProfileForm, SignUpForm


def register(request):
    if request.method == 'POST':

        firstname = request.POST['firstname']
        surename = request.POST['surename']
        username = request.POST['username']
        email = request.POST['email']
        city = request.POST['city']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        birth_date = request.POST['birth_date']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            # Check username
            if not len(password) >= 8:
                messages.error(
                    request, 'password must atleast be 8 charaters long!')
                return redirect('register')
            if not re.findall('[a-z]', password):
                messages.error(request, 'password myset contain lowercase!')
                return redirect('register')
            if not re.findall('[A-Z]', password):
                messages.error(request, 'password myset contain Uppercase!')
                return redirect('register')
            if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
                messages.error(request, 'password myset contain character!')
                return redirect('register')
            if not re.findall('\d', password):
                messages.error(request, 'password myset contain numbers!')
                return redirect('register')
            if models.UserProfile.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                if models.UserProfile.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    # Looks good
                    user = models.UserProfile.objects.create_user(
                        username=username, password=password, email=email,
                        firstname=firstname, lastname=surename, city=city,
                        address=address, phone_number=phone_number, birth_date=birth_date)
                    # Login after register
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('index')
                    user.save()
                    messages.success(
                        request, 'You are now registered and can log in')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'Form/register_form.html')


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'You are now registered and can log in')
            return redirect('login')
    else:
        form = SignUpForm()
    template_name = 'Form/register_form.html'
    return render(request, template_name, {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have successfully loged in!')
            return redirect('index_view_url')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('index_view_url')
    else:
        return redirect('index_view_url')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index_view_url')


def dashboard(request):
    # user_contacts = Contact.objects.order_by(
    #     '-contact_date').filter(user_id=request.user.id)

    # context = {
    #     'contacts': user_contacts
    # }
    return render(request, 'accounts/dashboard.htm')


def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("index")

    else:
        form = EditProfileForm(instance=request.user)
        args = {"form": form}
        return render(request, "accounts/edit_profile.htm", args)


# def update_profile(request):
#     args = {}

#     if request.method == 'POST':
#         form = UpdateProfile(request.POST)
#         form.actual_user = request.user
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('update_profile_success'))
#     else:
#         form = UpdateProfile()

#     args['form'] = form
#     return render(request, 'registration/update_profile.htm', args)
