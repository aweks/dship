import sha

from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class RegistrationManager(models.Manager):
    """
    Custom manager for the ``RegistrationProfile`` model.

    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.

    """
    def activate_user(self, request, user_id):
        """Activates a user by an administrator only."""
        if request.user.is_superuser \
           and request.user.is_active:
            # the user is logged in as a superuser so can activate
            # the account
            try:
                # get the profile associated with a given username
                #profile = self.get(id__exact=user_id)
                profile = User.objects.get(id__exact=user_id)
            except self.model.DoesNotExist:
                idjs
                return False
            user = profile
            user.is_active = True
            user.save()
            profile.save()
            return user
        # otherwise the user is not a superuser and thus can not activate
        # the account
        return False

    def create_inactive_user(self, username, password,
                             email, first_name, last_name,
                             send_email=True, profile_callback=None):
        """Creates an inactive user which is meant for admin activation."""
        new_user = User.objects.create_user(username, email, password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.is_active = False
        new_user.save()
        registration_profile = self.create_profile(new_user)

        if profile_callback is not None:
            profile_callback(user=new_user)

        if send_email:
            self._send_email(new_user, is_user=False)
            self._send_email(new_user, is_user=True)

        return new_user

    def _send_email(self, user, is_user=True):
        """Sends activation information via email to the user or admin.

        This was originally a part of create_inactive_user() but due to
        the length of the added code it was split off.
        """
        from django.core.mail import send_mail
        current_site = Site.objects.get_current()

        if is_user:
            # sends activation email to the user    
            subject = render_to_string('registration/activation_email_subject.txt',
                                   {'site':current_site})
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())

            message = render_to_string('registration/activation_email.txt',
                                   {'user_id':user.id,
                                   'site':current_site })

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                  [user.email])

        else:
            # sends activation email to the admin
            subject = render_to_string('registration/admin_activation_email_subject.txt',
                                   {'site':current_site})
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())

            message = render_to_string('registration/admin_activation_email.txt',
                                   {'user_id':user.id,
                                   'site':current_site })
            admin_email_list = []
            for i in settings.ADMINS:
                admin_email_list.append(i[1])

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                      admin_email_list)

    def create_profile(self, user):
        """Create a ``RegistrationProfileAdminActivated`` for a given
        ``User`` and return the ``RegistrationProfileAdminActivated``.
        """
        return self.create(user=user)

    def delete_expired_users(self):
        """
        Remove expired instances of ``RegistrationProfile`` and their
        associated ``User``s.

        Accounts to be deleted are identified by searching for
        instances of ``RegistrationProfile`` with expired activation
        keys, and then checking to see if their associated ``User``
        instances have the field ``is_active`` set to ``False``; any
        ``User`` who is both inactive and has an expired activation
        key will be deleted.

        It is recommended that this method be executed regularly as
        part of your routine site maintenance; this application
        provides a custom management command which will call this
        method, accessible as ``manage.py cleanupregistration``.

        Regularly clearing out accounts which have never been
        activated serves two useful purposes:

        1. It alleviates the ocasional need to reset a
           ``RegistrationProfile`` and/or re-send an activation email
           when a user does not receive or does not act upon the
           initial activation email; since the account will be
           deleted, the user will be able to simply re-register and
           receive a new activation key.

        2. It prevents the possibility of a malicious user registering
           one or more accounts and never activating them (thus
           denying the use of those usernames to anyone else); since
           those accounts will be deleted, the usernames will become
           available for use again.

        If you have a troublesome ``User`` and wish to disable their
        account while keeping it in the database, simply delete the
        associated ``RegistrationProfile``; an inactive ``User`` which
        does not have an associated ``RegistrationProfile`` will not
        be deleted.

        """
        #for profile in self.all():
        #    if profile.activation_key_expired():
        #        user = profile.user
        #        if not user.is_active:
        #            user.delete()
        pass

class RegistrationProfile(models.Model):
    """A clone of RegistrationProfile without the activation_key."""
    ACTIVATED = u"ALREADY_ACTIVATED"

    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))

    objects = RegistrationManager()

    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')

    def __unicode__(self):
        return u"Registration information for %s" % self.user

    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.

        Key expiration is determined by a two-step process:

        1. If the user has already activated, the key will have been
           reset to the string ``ALREADY_ACTIVATED``. Re-activating is
           not permitted, and so this method returns ``True`` in this
           case.

        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.

        """
        #expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return False
    activation_key_expired.boolean = True
