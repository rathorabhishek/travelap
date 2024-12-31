from django.contrib import admin
from .models import Questions,Choice,DriverDetail

# Register your models here.
admin.site.register(DriverDetail)
admin.site.register(Questions)
admin.site.register(Choice)
