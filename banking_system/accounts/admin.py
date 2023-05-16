from django.contrib import admin

from .models import BankAccountType, User, UserAddress, UserBankAccount, Keralabranch, Keraladistrict, District

admin.site.register(BankAccountType)
admin.site.register(User)
admin.site.register(UserAddress)
admin.site.register(UserBankAccount)
admin.site.register(Keraladistrict)
admin.site.register(Keralabranch)

class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(District,DistrictAdmin)




