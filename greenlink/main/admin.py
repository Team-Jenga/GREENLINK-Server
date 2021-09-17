from django.contrib import admin

from .models import Event, EventDetail, Favorite, Member, MemberAdmin, MemberUser

admin.site.register(Member)
admin.site.register(MemberAdmin)
admin.site.register(MemberUser)
admin.site.register(Event)
admin.site.register(EventDetail)
admin.site.register(Favorite)
