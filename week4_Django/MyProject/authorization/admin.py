from django.contrib import admin
from .models import Authorization


class AuthAdmin(admin.ModelAdmin):
  list_display = ("firstname", "lastname", "joined_date", "done", "phone")
  

admin.site.register(Authorization, AuthAdmin)