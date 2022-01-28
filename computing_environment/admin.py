from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp

from .models import User

from .models import Invitation
from .forms.invitation import InvitationAdminAddForm

admin.site.unregister(Site)
admin.site.unregister(Group)
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'last_login')}),
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
                'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'last_login')
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

from .models import Job
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creator', 'filename', 'state', 'is_private', 'created_at', 'updated_at')
    
    def filename(self, obj):
        return str(obj.program).split('_')[-1]

admin.site.register(Job, JobAdmin)

from .models import SubJob
from django.urls import reverse
from django.utils.html import format_html
class SubJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'link_to_job', 'link_to_worker', 'state', 'processor_usage',
                    'memory_usage','avg_processor_usage','avg_memory_usage','started_at', 
                    'created_at','last_worker_call')
    
    @admin.display(description="Job")
    def link_to_job(self, obj):
        link = reverse("admin:computing_environment_job_change", args=[obj.job.id])
        return format_html('<a href="{}">{}</a>', link, obj.job)

    @admin.display(description="Worker")
    def link_to_worker(self, obj):
        link = reverse("admin:computing_environment_worker_change", args=[obj.worker.id])
        return format_html('<a href="{}">{}</a>', link, obj.worker)

admin.site.register(SubJob,SubJobAdmin)


from .models import Worker
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address', 'processor', 'ram', 
                    'worked_time', 'created_at','updated_at')

admin.site.register(Worker,WorkerAdmin)