from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages

from computing_environment.forms import ProfileForm
from computing_environment.models import SubJob
from .dashboard_view import dashboard
from computing_environment.services import dashboard_stats

@login_required
def edit_profile(request):
    stats = dashboard_stats()
    recent_results = SubJob.objects.recent_results(request.user, 5)

    if request.POST:
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()

            messages.success(request, 'Profile successfully updated.')
            return redirect(dashboard)
    else:
        profile_form = ProfileForm(instance=request.user)

    context = { 'profile_form': profile_form, 'current_user': request.user,
                'stats': stats, 'recent_results': recent_results }
    return render(request, 'profile/edit.html', context)