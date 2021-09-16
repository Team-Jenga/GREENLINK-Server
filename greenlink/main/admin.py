from django.contrib import admin

from .models import Main, Member, MemberAdmin, MemberUser

admin.site.register(Main)
admin.site.register(Member)
admin.site.register(MemberAdmin)
admin.site.register(MemberUser)