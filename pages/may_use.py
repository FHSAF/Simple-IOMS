customer_id = request.POST.get('customer_id')
contract_duration = request.POST['contract_duration']
device_offer = request.POST.get('device_offer')
device_used = request.POST.get('device_used')
charge_per_month = request.POST.get('charge_per_month')
device_charge = request.POST.get('device_charge')
paymet_currency = request.POST.get('paymet_currency')
extra_fees = request.POST.get('extra_fees')
money_paid = request.POST.get('paid_money')
package_used = request.POST.get('package_used')
customer_net_usecase = request.POST.get('customer_net_usecase')
acquaintance_method = request.POST.get('acquaintance_method')
document = request.POST.get('document')
description = request.POST.get('description')

contract_duration = time.mktime(datetime.datetime.strptime(contract_duration, "%d/%m/%Y").timetuple())

print("_____________________________________", contract_duration)

package_used = get_object_or_404(PACKAGE_TYPE, id=package_used)


customer_info = get_object_or_404(CUSTOMER_INFO, customer_id=customer_id)

customer = CUSTOMER_CONTRACT_INFO.objects.create(
    customer_personal_info=customer_info,
    contract_duration=contract_duration,
    device_offer=device_offer,
    device_used=device_used,
    charge_per_month=charge_per_month,
    device_charge=device_charge,
    paymet_currency=paymet_currency,
    extra_fees=extra_fees,
    paid_money=money_paid,
    package_used=package_used,
    customer_net_usecase=customer_net_usecase,
    acquaintance_method=acquaintance_method,
    document=document,
    description=description
)

last_contract = get_object_or_404(CUSTOMER_CONTRACT_INFO, customer_personal_info=customer_info)
if last_contract:
    customer.contract_period += last_contract.contract_period
else:
    customer.contract_period += 1

print("________________________________{}________________________________".formt(contract_duration))

customer.save()
