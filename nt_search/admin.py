from django.contrib import admin
from .models import Response
# Register your models here.

class ResponseAdmin(admin.ModelAdmin):
    list_display = ['sequence']

admin.site.register(Response, ResponseAdmin)