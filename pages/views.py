from django.shortcuts import render, redirect

from django.shortcuts import render, get_object_or_404
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from django.views.generic import ListView
from .models import *
from .forms import *
from django.contrib import messages
from IOMS.models import *
from .render import Render
from django.views.generic import View

def index_view(request):

    if not request.user.id is None:
        print(request.user, '>>>>>>>>>>>>>>>.')
        employer = get_object_or_404(EMPLOYERS_INFO, user_id=request.user.id)
        print('_____________________', request.user.employer_info_user)
        context = {
            'employer': employer,
        }
    else:
        context = {
            'employer': 'empty',
        }
    return render(request, 'pages/index.htm', context)

def CustomerCreate(request):
    if request.method == "POST":
        forms = CreateCustomer(request.POST, request.FILES or None)
        customer_id = request.POST.get('customer_id')
        if CUSTOMER_INFO.objects.filter(customer_id=customer_id).exists():
            messages.error(request, 'Customer with ID {} already exsits!'.format(customer_id))
        if forms.is_valid():
            print('valid_______________________________________')

            customer = forms.save(commit=False)
            # melk.realtor = get_object_or_404(Realtor, user_id=request.user.id)

            customer.save()
            print("________________________________saved_______________________________________")
        # messages.success(request, "Registration Successfully!")
            return redirect("index_view_url")
    else:
        forms = CreateCustomer()

    current_user = request.user

    employer = get_object_or_404(EMPLOYERS_INFO, user_id=current_user.id)

    context = {
        "form": forms,
        "employer": employer
    }
    return render(request, "forms/customer_info_form.html", context)

def CustomerContract(request):

    if request.method == "POST":
        form = CustomerContractForm(request.POST, request.FILES or None)
        if form.is_valid():



            print("________________________________form is valid_______________________________________")
            customer = form.save(commit=False)

            customer_info = get_object_or_404(CUSTOMER_INFO, customer_id=request.POST.get('customer_id'))
            customer.customer_personal_info = customer_info


            if CUSTOMER_CONTRACT_INFO.objects.filter(customer_id=request.POST.get('customer_id')).exists():
                previous_contract = CUSTOMER_CONTRACT_INFO.objects.filter(customer_id=request.POST.get('customer_id')).order_by('-updated_at')[0]

                customer.contract_period = int(previous_contract.contract_period) + 1
                previous_contract.expired = True
                previous_contract.save()
            else:
                customer.contract_period += 1


            customer.save()


        # messages.success(request, "Registration Successfully!")
        return redirect("report_url")
    else:
        form = CustomerContractForm()
    current_user = request.user

    employer = get_object_or_404(EMPLOYERS_INFO, user_id=current_user.id)

    context = {
        "form": form,
        "employer": employer
    }
    return render(request, "forms/customer_contract_form.html", context)


def user_profile(request):

    current_user = request.user

    employer = get_object_or_404(EMPLOYERS_INFO, user_id=current_user.id)
    print(current_user.id, '<<<<<<<<<<<<<<<<<<<<<<,', employer)
    context = {
        'employer': employer,
    }
    return render(request, 'accounts/profile.html', context)


def installation_view(request):
    current_user = request.user
    employer = get_object_or_404(EMPLOYERS_INFO, user_id=current_user.id)
    if request.method == 'POST':
        form = InsTroubForm(request.POST)
        action_type = request.POST.get('action_type')
        customer_id = request.POST.get('customer')
        fault_observed = request.POST.get('fault_observed')
        action_taken = request.POST.get('action_taken')
        from_time = request.POST.get('from_time')
        to_time = request.POST.get('to_time')

        tech_eng = employer
        customer = CUSTOMER_CONTRACT_INFO.objects.filter( customer_personal_info_id=customer_id).order_by('-updated_at')
        print('_______________________________________', customer)
        if not customer:
            messages.error(request, 'No Customer Found with such ID!')
            return redirect('ins_trob_url')

        customer = customer[0]

        device_used = request.POST.get('device_used')

        err = None

        if device_used == '0':
            device_used = device_used
        else:
            if '/' in device_used:
                devices = device_used.split('/')
                for d in devices:
                    device = Devices.objects.filter(unique_parameter=d)
                    if device.exists():
                        if device.outed == True:
                            messages.error(request, 'The device with MAC {} is already used!'.format(d))
                            err = 1
                        else:
                            device.outed = True

                    else:
                        messages.error(request, 'The device with MAC {} does not exist!'.format(d))
                        err = 1
            else:
                device = Devices.objects.filter(unique_parameter=device_used)
                if device.exists():
                    if device.outed == True:
                        messages.error(request, 'The device with MAC {} is already used!'.format(device_used))
                        err = 1
                    else:
                        device.outed = True

                else:
                    messages.error(request, 'The device with MAC {} does not exist! \n MAC with specified format'.format(device_used))
                    err = 1


        if err is None:
            ITM = Ins_Trob_REPORT.objects.create(
                tech_eng=tech_eng,
                action_type=action_type,
                fault_observed=fault_observed,
                action_taken=action_taken,
                from_time=from_time,
                to_time=to_time,
                customer=customer,
                device_used=device_used
            )
            print("________________________________form")

            ITM.save()

            return redirect("report_url")

    else:
        form = InsTroubForm()

    context = {
        'employer': employer,
        'form': form
    }
    return render(request, 'forms/ins_trob.html', context)


def Report(request):

    customers = CUSTOMER_CONTRACT_INFO.objects.all().order_by('-updated_at').filter(expired=False)
    current_user = request.user
    employer = get_object_or_404(EMPLOYERS_INFO, user_id=current_user.id)
    context = {
        'customers': customers,
        'employer': employer,
    }
    return render(request, 'pages/reports.html', context)


def InputStockView(request):

    current_user = request.user
    employer = get_object_or_404(EMPLOYERS_INFO, user_id=current_user.id)

    if request.method == "POST":
        input_by = current_user
        input_type = request.POST.get('input_type')
        good_name = request.POST.get('good_name')
        quantity = request.POST.get('quantity')
        device_status = request.POST.get('device_status')
        date_in = request.POST.get('date_in')
        price = request.POST.get('price')
        currency = request.POST.get('currency')

        IS = InputStock.objects.create(
            input_by=input_by,
            input_type=input_type,
            good_name_id=good_name,
            quantity=quantity,
            device_status=device_status,
            date_in=date_in,
            price=price,
            currency=currency
        )
        IS.save()
        return redirect('index_view_url')
    else:
        form = InputStockForm()
    constext = {
        'form': form,
        'employer': employer
    }

    return render(request, 'forms/input_stock.html', constext)

def RecordView(request):
    current_user = request.user
    employer = get_object_or_404(EMPLOYERS_INFO, user_id=current_user.id)
    to_berecorded = InputStock.objects.filter(seperable=True).filter(recorded=False)

    deviceItems = {}
    for IS in to_berecorded:
        deviceItems[IS.quantity-IS.number_recorded] = IS.good_name
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%',deviceItems)
    count = to_berecorded.count()

    if request.method == "POST":
        form = RecordForm(request.POST)
        recorded_by = employer
        device_name = request.POST.get('device_name')
        unique_parameter = request.POST.get('unique_parameter')

        if Devices.objects.filter(unique_parameter=unique_parameter).exists():
            messages.error(request, 'MAC address {} is already exists'.format(unique_parameter))
            return redirect('record-url')

        print(device_name,'<________________________________')

        device = Devices.objects.create(
            recorded_by=recorded_by,
            device_name_id=device_name,
            unique_parameter=unique_parameter,
        )

        device.save()
        return redirect('record-url')
    else:
        form = RecordForm()
    context = {
        'to_berecorded': to_berecorded,
        'count': count,
        'employer': employer,
        'form': form,
        'deviceItems': deviceItems,
    }

    return render(request, 'forms/record_form.html', context)


class CustomerListView(ListView):
    model = Customer
    template_name = 'customer/main.html'



def CustomerContractReport(request, *args, **kwargs):
    pk = kwargs.get('pk')
    customers = get_object_or_404(CUSTOMER_CONTRACT_INFO, pk=pk)
    context = {
        'customers': customers
    }
    return render(request, 'forms/customer_contract.html', context)

#
# class CustomerContractReport(View):
#
#     def get(self, request, pk):
#         customers = get_object_or_404(CUSTOMER_CONTRACT_INFO, pk=pk)
#         params = {
#             'customers': customers
#         }
#         return Render.render('pdf.html', params)

def render_pdf_view(request):
    template_path = 'customer/pdf1.html'
    context = {'my_var': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if want to download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if want to display it in the browser
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
