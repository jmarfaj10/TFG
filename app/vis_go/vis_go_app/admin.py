from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Log, Mission, Prompt, Goal

admin.site.register(User, UserAdmin)
admin.site.register(Log)
admin.site.register(Mission)
admin.site.register(Prompt)
admin.site.register(Goal)
