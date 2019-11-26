from django.contrib import admin

from reminder.models import FDAccountDetail, Interest
# Register your models here.

admin.site.register([FDAccountDetail, Interest])