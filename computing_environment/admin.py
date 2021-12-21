from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms

from .models import User

from .models import Invitation
from .forms.invitation import InvitationAdminAddForm

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser',
            'groups', 
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'name', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'inviter', 'sent', 'accepted')

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = InvitationAdminAddForm
        kwargs['form'].user = request.user
        kwargs['form'].request = request
        return super(InvitationAdmin, self).get_form(request, obj,  **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
         if db_field.name == "inviter":
                 kwargs["queryset"] = User.objects.filter(is_staff=True)
         return super(InvitationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Invitation, InvitationAdmin)