from django import forms
from .models import *
from IOMS.models import *


class CreateCustomer(forms.ModelForm):
    class Meta:
        model = CUSTOMER_INFO
        exclude = ("user", "created_at", "updated_at",)


        widgets = {
            'customer_id': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Customer ID'}),
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Customer firstname...'}),
            'surename': forms.TextInput(attrs={'class': 'form-control','placeholder':'family or surename...'}),
            'N_ID_NO': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Tazkira number required ...'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'customer_type': forms.Select(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Occupation of customer...'}),
            'address': forms.Textarea(attrs={'class': 'form-control','placeholder': "Exact Current Address of Customer ..."}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Must be entered in format +9399999999...'}),
            'phone_number_backup': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Must be entered in format +9399999999...'}),
            'email_add': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address (username@domain.com)...'}),

            'country': forms.TextInput(attrs={'class': 'form-control','placeholder':'Country required for foriegner customer...'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Passport number required for foriegner customer ...'}),
            # 'photo': forms.FileInput(attrs={'class': 'form-control-file'}),

        }



class CustomerContractForm(forms.ModelForm):

    class Meta:
        model = CUSTOMER_CONTRACT_INFO
        exclude = ("customer_personal_info", "created_at", "updated_at","contract_period")


        widgets = {
            'customer_id': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Customer ID'}),
            'contract_duration': forms.TimeInput(attrs={'class': 'form-control','placeholder':'Enter (ex: 30 days) format...'}),
            'device_used': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Tazkira number required ...'}),
            'device_offer': forms.Select(attrs={'class': 'form-control'}),

            'charge_per_month': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Charge of internet package monthly...'}),
            'device_charge': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Device charge ... '}),
            'paid_money': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Amount of money paid by the time signing contract ...'}),
            'extra_fees': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Any extra fees ...'}),
            'paymet_currency': forms.Select(attrs={'class': 'form-control'}),

            'description': forms.Textarea(attrs={'class': 'form-control','placeholder': "Exact Current Address of Customer ..."}),
            'acquaintance_method': forms.Select(attrs={'class': 'form-control'}),
            'package_used': forms.Select(attrs={'class': 'form-control'}),
            'customer_net_usecase': forms.Select(attrs={'class': 'form-control'}),
            }

class InputStockForm(forms.ModelForm):
    good_name = forms.ModelChoiceField(queryset=GoodNames.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    device_from = forms.ModelChoiceField(queryset=Supliyer.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    bill = forms.ImageField()

    class Meta:
        model = InputStock
        exclude = ('input_by', 'created_at', 'updated_at', 'number_recorded')

        widgets = {

            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Total number bought...'}),
            'device_status': forms.Select(attrs={'class': 'form-control'}),
            'input_type': forms.Select(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Total price...'}),
            }


class InsTroubForm(forms.ModelForm):
    class Meta:
        model = Ins_Trob_REPORT
        exclude = ('tech_eng', 'created_at', 'from_time', 'to_time')

        widgets = {
            'action_type': forms.Select(attrs={'class': 'form-control'}),
            'customer': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Insert customer ID ...'}),
            'fault_observed': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Explain in details ...'}),
            'action_taken': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Explain in details ...'}),
            'device_used': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'xx:xx:xx:xx:xx:xx/yy:yy:yy:yy:yy:yy or 0'}),
            'cable': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'in meteres...'}),
            'signal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'in Tx/Rx fromat ...'}),
            'radio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Radion 6 ...'}),
            'stand': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Ex: 1 meter iron stand...'}),
        }

class RecordForm(forms.ModelForm):

    device_name = forms.ModelChoiceField(InputStock.objects.filter(seperable=True).filter(recorded=False), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Devices
        exclude = ('recorded_at', 'recorded_by', 'outed')

        widgets = {
            'unique_parameter': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Device MAC(xx:xx:xx:xx:xx:xx) address ...'}),
        }
