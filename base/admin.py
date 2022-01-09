from django.contrib import admin

# Register your models here.
from .models import Invoice

# To check the data on admin panel
admin.site.register(Invoice)