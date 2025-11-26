from django.contrib import admin

from .models import User, UserCounter

# Register your models here.

admin.site.register([User, UserCounter])
