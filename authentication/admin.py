# Third-party imports
from django.contrib import admin

# Local imports
from .models import User


# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number')
    fields = ('username', 'phone_number')


admin.site.register(User, CustomUserAdmin)
