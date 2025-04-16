from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Seller, Client

class SellerAdmin(UserAdmin):
    model = Seller
    list_display = ['email', 'name', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональные данные', {'fields': ('name',)}),  # Исправлено
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name'),  # Кортеж
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('inn', 'last_name', 'first_name', 'created_at')
    search_fields = ('inn', 'last_name', 'first_name')
    list_filter = ('created_at',)


admin.site.register(Seller, SellerAdmin)