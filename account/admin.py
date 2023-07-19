from django.contrib import admin
from account.models import Contact, Logo, PageCommon, LinkManagement, User, Video, Linktype
# Register your models here.

# class UserArea(admin.ModelAdmin):
#     pass
class UserDetailsAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(UserDetailsAdmin, self).get_changeform_initial_data(request)
        get_data['upload_by'] = request.user.pk
        return get_data

admin.site.register(User)
admin.site.register(Video, UserDetailsAdmin)
admin.site.register(Contact)
admin.site.register(PageCommon)
admin.site.register(LinkManagement)
admin.site.register(Linktype)
admin.site.register(Logo)
