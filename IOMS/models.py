from django.db import models
from accounts.models import UserProfile

from django.core.validators import RegexValidator
from django.utils import timezone

from pages.models import EMPLOYERS_INFO, Ins_Trob_REPORT, CUSTOMER_CONTRACT_INFO

class GoodNames(models.Model):
    vendor_name = models.CharField(max_length=50)

    good_model = models.CharField(max_length=50)

    other_descriptions = models.TextField()

    def __str__(self):
        return str(self.vendor_name + " " + self.good_model)

class Supliyer(models.Model):
    company_name = models.CharField(max_length=100)
    res_person = models.CharField(max_length=100)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)
    email_add = models.EmailField(max_length=255)

    def __str__(self):
        return str(self.company_name)




class InputStock(models.Model):
    input_by = models.ForeignKey(UserProfile, related_name='buyer', on_delete=models.CASCADE)

    input_type = models.CharField(choices=(('Reciever', 'Reciever'), ('Cable', 'Cable'), ('Ap', 'Ap'), ('PowreBank', 'PowreBank'), ('Others', 'Others')), max_length=15)

    good_name = models.ForeignKey(GoodNames, related_name="devices", on_delete=models.RESTRICT)

    seperable = models.BooleanField(default=False)

    quantity = models.IntegerField()
    number_recorded = models.IntegerField(default=0)

    device_status = models.CharField(choices=(('New', 'New'), ('Back_From_Customer', 'Back From Customer'),('Used', 'Used')), max_length=30)

    device_from = models.ForeignKey(Supliyer, related_name='Supliyer_r', on_delete=models.RESTRICT, null=True)
    date_in = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    price = models.IntegerField()
    currency = models.CharField(choices=(('USD', 'USD'), ('AFN', 'AFN')), max_length=10)

    bill = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True, default=None)

    def recored(self):
        return (self.quantity==self.number_recorded)
    recorded = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.recored():
            self.recorded = True
            super(InputStock, self).save(*args, **kwargs)
        else:
            super(InputStock, self).save(*args, **kwargs)




    def __str__(self):
        return str(self.good_name.vendor_name)


class Devices(models.Model):
    device_name = models.ForeignKey(InputStock, related_name="devices_inputStock", on_delete=models.RESTRICT)
    recorded_by = models.ForeignKey(EMPLOYERS_INFO, related_name='dvice_recoder', on_delete=models.RESTRICT)
    unique_parameter = models.CharField(max_length=50)
    recorded_at = models.DateTimeField(auto_now_add=True)
    outed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if Devices.objects.filter(unique_parameter=self.unique_parameter).exists():

            super(Devices, self).save(*args, **kwargs)
        else:
            if Devices.objects.filter(id=self.id).exists():
                super(Devices, self).save(*args, **kwargs)
            else:
                IS = self.device_name
                IS.number_recorded += 1
                IS.save()
                super(Devices, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        IS = self.device_name
        IS.number_recorded -= 1
        IS.recorded = False
        IS.save()
        super(Devices, self).delete(*args, **kwargs)


    def __str__(self):
        return str(self.device_name.input_type)

class DeviceConsumed(models.Model):
    consumer_for = models.ForeignKey(Ins_Trob_REPORT, related_name="device_consumed_Ins_Trob_REPORT", on_delete=models.RESTRICT, null=True)
    consumed_customer = models.ForeignKey(CUSTOMER_CONTRACT_INFO, related_name='devices_customer_constract_info', on_delete=models.RESTRICT, null=True)
    device_name = models.ForeignKey(Devices, related_name='DeviceConsumed_Devices', on_delete=models.RESTRICT)
    consumed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.device_name.device_name.input_type)



class MoneySpent(models.Model):
    spent_by = models.ForeignKey(EMPLOYERS_INFO, related_name="money_spent_employer", on_delete=models.RESTRICT)
    amount = models.IntegerField()
    currency = models.CharField(choices=(('USD', 'USD'), ('AFN', 'AFN')), max_length=10)
    spent_for = models.CharField(max_length=50)


    spent_at = models.DateTimeField()

    def __str__(self):
        return str(self.amount)


class MoneyReciept(models.Model):
    amount = models.IntegerField()
    currency = models.CharField(choices=(('USD', 'USD'), ('AFN', 'AFN')), max_length=10)
    recieved_for = models.CharField(max_length=50)
    recieved_by = models.ForeignKey(EMPLOYERS_INFO, related_name="money_recieved_employer", on_delete=models.RESTRICT)

    recived_at = models.DateTimeField()

    def __str__(self):
        return str(self.amount)
