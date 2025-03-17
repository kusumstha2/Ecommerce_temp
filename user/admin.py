from django.contrib import admin
from .models import User

class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['email', 'username', 'phone', 'role', 'is_active']
    search_fields = ['email', 'username', 'phone']
    
    # Modify or remove the ordering field
    ordering = ['email']  # For example, order by email instead of username

admin.site.register(User, CustomUserAdmin)
