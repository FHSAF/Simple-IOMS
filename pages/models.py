from django.db import models
from accounts.models import UserProfile
from django.core.validators import RegexValidator
from datetime import datetime
from django.utils import timezone

# from IOMS.models import Devices

# my_model.duration = datetime.timedelta(days=20, hours=10)
from multiselectfield import MultiSelectField


# Create your models here.
job_departments = (
    ('Financial', 'Financial'),
    ('Technical', 'Technical'),
    ('Marketting', 'Marketting'),
    ('General', 'General')
)
job_level = (
    ('A', 'CHRO, CEO'),
    ('B', 'COO, Vice President'),
    ('C', 'Director'),
    ('D', 'Manager'),
    ('E', 'Individual Contributer'),
    ('F', 'Entry-Level')
)


class EMPLOYERS_INFO(models.Model):
    # personal information
    user = models.OneToOneField(
        UserProfile, related_name='employer_info_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surename = models.CharField(max_length=255)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    N_ID_NO = models.IntegerField()
    passport_number = models.CharField(max_length=10)
    # Company information
    job_department = models.CharField(choices=job_departments, max_length=15)
    job_title = models.CharField(max_length=200)
    job_level = models.CharField(choices=job_level, max_length=30)
    salary = models.IntegerField()
    descriptions = models.TextField()
    entry_date = models.DateTimeField()
    form_submition_date = models.DateTimeField(default=datetime.now)

    out_date = models.DateTimeField(blank=True, null=True)
    #

    def __str__(self):
        return self.name + " " + self.surename


class PACKAGE_TYPE(models.Model):
    _type = models.CharField(
        choices=(('Limited', 'Limited'), ('Unlimited', 'Unlimited')), max_length=15)
    amount = models.CharField(max_length=15)
    speed = models.CharField(max_length=10)
    validity = models.DurationField(max_length=10)
    price = models.IntegerField()

    def __str__(self):
        return str(self._type + " " + self.amount)


class CUSTOMER_INFO(models.Model):
    user = models.ForeignKey(
        UserProfile, related_name='customer_info_user', on_delete=models.CASCADE, null=True)

    customer_type = models.CharField(
        choices=(('Real', 'Real'), ('Legal', 'Legal')), max_length=30)

    customer_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    surename = models.CharField(max_length=255)
    gender = models.CharField(
        choices=(('Male', 'Male'), ('Female', 'Female')), max_length=10)
    N_ID_NO = models.IntegerField(blank=True)

    occupation = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)
    phone_number_backup = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)
    email_add = models.EmailField(max_length=255, null=True, default=None)
    # for foriegner only
    country = models.CharField(max_length=50, null=True, default=None)
    passport_number = models.CharField(max_length=10, null=True, default=None)
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/', blank=True, null=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name + " " + str(self.customer_id))

# for Technical department


class CUSTOMER_CONTRACT_INFO(models.Model):
    """docstring forCUSTOMER_CONTRACT_INFO."""
    customer_personal_info = models.ForeignKey(
        CUSTOMER_INFO, related_name='Customer_contract', on_delete=models.CASCADE)
    device_offer = models.CharField(choices=(
        ("lease", "Lease"), ('sold', 'Sold'), ('owned', 'owned')), max_length=50)
    # device_used = models.CharField(max_length=200)
    contract_period = models.IntegerField(default=0)
    contract_duration = models.DurationField()

    device_choices = (('reciever', 'reciever'), ('AP', 'AP'),
                      ('Cable', 'Cable'), ('others', 'others'), ('None', 'None'))
    devices_used = MultiSelectField(
        choices=device_choices, max_length=50)

    customer_id = models.IntegerField()

    expired = models.BooleanField(default=False)

    charge_per_month = models.IntegerField()
    device_charge = models.IntegerField()
    paid_money = models.IntegerField()
    extra_fees = models.IntegerField()
    paymet_currency = models.CharField(
        choices=(('USD', 'USD'), ("AFN", "AFN")), max_length=20)

    package_used = models.ForeignKey(
        PACKAGE_TYPE, related_name='Package_type_contract', on_delete=models.CASCADE)
    customer_net_usecase = models.CharField(
        choices=(('Home', 'Home'), ('Enterprise', 'Enterprise')), max_length=15)
    description = models.CharField(max_length=200)

    document_copy_choices = (('تذکزه', 'تذکره'), ('پاسپوت', 'پاسپوت'),
                             ('جواز', 'جواز'), ('کارت هویت دگر', 'کارت هویت دگر'))

    document = MultiSelectField(
        choices=document_copy_choices,
        max_choices=4,
        min_choices=1,
        max_length=50
    )

    acquaintance_method = models.CharField(choices=(('Social Media', 'Social Media'), ('Friends', 'Friends'),
                                                    ('Billboard', 'Billboard'), ('Ad Paper', 'Ad Paper')), max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_dept(self):
        return self.charge_per_month + self.device_charge + self.extra_fees - self.paid_money

    def exp_date(self):
        return self.contract_duration - (timezone.now() - self.updated_at)

    def __str__(self):
        return str(self.customer_personal_info.name + ' ' + self.package_used._type)


#  for Technical department
#
# class PACKAGES_OUT(models.Model):
#     customer = models.ForeignKey(CUSTOMER_CONTRACT_INFO, related_name='Customer', on_delete=models.CASCADE)
#     package_type = models.ForeignKey(PACKAGE_TYPE, related_name='Package_Type', on_delete=models.CASCADE)
#     contract_duration = models.DurationField()
#     total_money = models.IntegerField()
#     money_paid = models.IntegerField()
#
#     def money_dept(self):
#         return self.total_money - self.money_paid
#
#
#     def __str__(self):
#         return str(self.customer.name + " " + self.package_type._type)


class DAILY_REPORT(models.Model):
    employer = models.ForeignKey(
        EMPLOYERS_INFO, related_name='Employer', on_delete=models.CASCADE)

# extra


class Customer(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField()
    description = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

# end extra


class Ins_Trob_REPORT(models.Model):
    tech_eng = models.ForeignKey(EMPLOYERS_INFO, on_delete=models.RESTRICT)
    action_type = models.CharField(choices=(('Installation', 'Installation'),
                                            ('Troubleshooting', 'Troubleshooting')), max_length=20)
    customer = models.ForeignKey(
        CUSTOMER_CONTRACT_INFO,  related_name='Customer_Ins_Trob', on_delete=models.CASCADE)

    fault_observed = models.TextField()
    action_taken = models.TextField()

    from_time = models.DateTimeField()
    to_time = models.DateTimeField()

    radio = models.CharField(max_length=20)
    signal = models.CharField(max_length=50)
    cable = models.IntegerField()
    stand = models.CharField(max_length=50, default='None')

    device_used = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.action_type + ' ' + self.customer.customer_personal_info.name)
