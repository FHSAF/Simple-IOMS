from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator


class UserProfileManager(BaseUserManager):
    """Manager for User profiles"""

    def create_user(self, email, firstname, password=None, **extra_fields):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, firstname, password, **extra_fields):
        """Create and save a new superuser with"""
        user = self.create_user(email, firstname, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)  # validators should be a list


    gender = models.CharField(choices=(("Male", "Male"),("Female", "Femal")), max_length=10)


    is_financial_employer = models.BooleanField(default=False)
    is_technical_employer = models.BooleanField(default=False)

    is_cfo = models.BooleanField(default=False)
    is_cto = models.BooleanField(default=False)

    is_activated = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname',]

    # django to interact with our custom model
    def get_full_name(self):
        """ Retrieve full name of user"""
        return self.firstname + " " + self.lastname

    def get_short_name(self):
        """Retreive full name of user"""
        return self.firstname

    def __str__(self):
        """Return string representation of our user"""
        return self.firstname + " " + self.lastname


# Create your models here.
class ProfileFeedItem(models.Model):
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status_text
