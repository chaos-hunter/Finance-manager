from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User

# Unregister the default User admin so we can customize it
admin.site.unregister(User)

# Register our custom User admin
@admin.register(User)
class CustomUserAdmin(DefaultUserAdmin):
    # This ensures we see 'date_joined' (account creation time) in the user list table
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    
    # We also add 'date_joined' to filters so you can easily sort/filter users by account creation time
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'date_joined')
