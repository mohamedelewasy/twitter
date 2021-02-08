from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Account,
)

class AdminAccount(UserAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    readonly_fields = ('id', 'password', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, admin_class=AdminAccount)