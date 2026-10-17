from django.contrib import admin
from .models import SusuGroup, GroupMember, MemberContribution, WeekPayout

admin.site.register(SusuGroup)
admin.site.register(GroupMember)
admin.site.register(MemberContribution)
admin.site.register(WeekPayout)