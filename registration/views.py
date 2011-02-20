"""
Views which allow users to create and activate accounts.

"""


from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from registration.forms import RegistrationFormUserNameIsEmail
from registration.models import RegistrationProfile

def activate(request, activate_user_id,
             template_name='registration/activate.html',
             extra_context=None):
    """Requires an administrator to activate a specified username."""
    account = RegistrationProfile.objects.activate_user(request, activate_user_id)

    if extra_context is None:
        extra_context = {}

    context = RequestContext(request)

    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                    {'account':account,
                     'expiration_days':settings.ACCOUNT_ACTIVATION_DAYS},
                     context_instance=context)

def register(request, success_url=None,
                      form_class=RegistrationFormUserNameIsEmail,
                      profile_callback=None,
                      template_name='registration/registration_form.html',
                      extra_context=None):
    """A new registration method that starts the process off."""
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save(profile_callback=profile_callback)
            # success_url needs to be dynamically generated here; setting a
            # a default value using reverse() will cause circular-import
            # problems with the default URLConf for this application, which
            # imports this file.
            return HttpResponseRedirect(success_url or
                                    reverse('registration_complete'))
    else:
        form = form_class()

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)

    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                             {'form':form},
                              context_instance=context)
