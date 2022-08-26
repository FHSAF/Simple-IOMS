from django.contrib import admin

from . import models
admin.site.register(models.EMPLOYERS_INFO)
admin.site.register(models.PACKAGE_TYPE)
admin.site.register(models.CUSTOMER_INFO)

admin.site.register(models.CUSTOMER_CONTRACT_INFO)

# admin.site.register(models.PACKAGES_OUT)
admin.site.register(models.DAILY_REPORT)
admin.site.register(models.Ins_Trob_REPORT)


# admin.site.register(models.Feed)
