from django.db import models
from django.db.models.deletion import SET_NULL
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.sites.models import Site
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from computing_environment.models.user import User

class Invitation(models.Model):
    class Meta:
        app_label = "computing_environment"

    email = models.EmailField(max_length=254, unique=True)
    token = models.CharField(max_length=64, unique=True)
    accepted = models.BooleanField(default=False)
    inviter = models.ForeignKey(User, null=True, blank=True, on_delete=SET_NULL) 
    sent = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, email, inviter=None, **kwargs):
        token = get_random_string(64).lower()
        instance = cls._default_manager.create(
            email=email,
            token=token,
            inviter=inviter,
            **kwargs)
        return instance

    def send_invitation(self, request, **kwargs):
        current_site = kwargs.pop('site', Site.objects.get_current())
        invite_url = reverse('account_sign_up', args=[self.token])
        invite_url = request.build_absolute_uri(invite_url)
        ctx = kwargs
        ctx.update({
            'invite_url': invite_url,
            'site_name': current_site.name,
            'email': self.email,
            'token': self.token,
            'inviter': self.inviter,
        })

        email_subject = render_to_string('invitations/email/email_invite_subject.txt', ctx)
        email_message = render_to_string('invitations/email/email_invite_message.txt', ctx)

        send_mail(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [self.email])
        self.sent = timezone.now()
        self.save()

    def __str__(self):
        return "Invite: {0}".format(self.email)