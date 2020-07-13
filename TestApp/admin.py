from django.contrib import admin
from TestApp.models import Profile,CompanyAddress,PermanentAddress,Friends
from django.utils.html import mark_safe
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['profile_id','name','phone_no','gender','date_of_birth','profilepic']
    list_filter = ('name','gender')
    search_fields = ('name','gender')
    readonly_fields = ('profilepicture',)

    def profilepicture(self,object):
        return mark_safe("<img src='{url}' width='200' height='200'/>".format(url=object.profilepic.url))


class CompanyAddressAdmin(admin.ModelAdmin):
    list_display = ['user_id','street_address','city','state','pincode','country']
    list_filter = ('city','street_address')
    search_fields = ('city','street_address')

class PermanentAddressAdmin(admin.ModelAdmin):
    list_display = ['user_id','street_address','city','state','pincode','country']
    list_filter = ('city','street_address')
    search_fields = ('city','street_address')

class FriendsAdmin(admin.ModelAdmin):
    list_display = ['profile_id','name']

admin.site.register(Profile,ProfileAdmin)
admin.site.register(CompanyAddress,CompanyAddressAdmin)
admin.site.register(PermanentAddress,PermanentAddressAdmin)
admin.site.register(Friends,FriendsAdmin)
