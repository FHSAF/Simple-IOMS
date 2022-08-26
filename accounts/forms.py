from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import validators

from .models import UserProfile
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.validators import RegexValidator


class SignUpForm(UserCreationForm):

    firstname = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'placeholder': 'your name ...'}))
    surename = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'placeholder': 'your lastname ...'}))
    gender = forms.ChoiceField(choices=(("Male", "Male"),("Female", "Femal")), widget=forms.TextInput(attrs={'placeholder': 'gender ...'}))
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(
        attrs={'placeholder': 'your email address ...'}))
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'placeholder': 'your address(Ex: Kabul, 13th-district ...'}))
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(
        validators=[phone_regex], max_length=17, widget=forms.NumberInput(
            attrs={'placeholder': 'your contact number(Ex: +93777777777)...'}))  # validators should be a list
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={'placeholder': 'password ...'}), validators=[validate_password])
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={'placeholder': 'repeat password ...'}), validators=[validate_password])

    class Meta:
        model = UserProfile
        fields = ('firstname', 'gender', 'email', 'birth_date', 'phone_number', 'address','password1',
                  'password2')


class EditProfileForm(UserChangeForm):

    class Meta:
        model = UserProfile
        fields = {
            "email",
            "firstname",
            "lastname",
        }


# class UpdateProfile(forms.ModelForm):
#     username = forms.CharField(required=True)
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(required=False)
#     last_name = forms.CharField(required=False)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name')

#     def clean_email(self):
#         username = self.cleaned_data.get('username')
#         email = self.cleaned_data.get('email')

#         if email and User.objects.filter(email=email).exclude(username=username).count():
#             raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
#         return email

#     def save(self, commit=True):
#         user = super(RegistrationForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']

#         if commit:
#             user.save()

#         return user
