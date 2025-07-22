from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import CreateView
from django.conf import settings
from .forms import SignUpForm, ProfileForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        # 1) Create the user as inactive
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # 2) Build the activation link
        current_site = get_current_site(self.request)
        uid   = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_path = reverse(
            'activate',
            kwargs={'uidb64': uid, 'token': token}
        )
        activation_link = f"{self.request.scheme}://{current_site.domain}{activation_path}"

        # 3) Send the email
        subject = "Activate Your Finance Manager Account"
        message = render_to_string('accounts/activation_email.html', {
            'user': user,
            'activation_link': activation_link,
        })
        send_mail(subject, message, None, [user.email])

        # 4) Render a “check your inbox” page
        return render(self.request, 'accounts/activation_sent.html', {
            'email': user.email
        })


def activate_account(request, uidb64, token):
    """
    View that’s hit when the user clicks the activation link.
    """
    try:
        uid  = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        # Explicitly tell Django which auth backend to use:
        login(
            request,
            user,
            backend='accounts.backends.EmailOrUsernameModelBackend'
        )

        return render(request, "accounts/activation_complete.html")
    else:
        return render(request, "accounts/activation_invalid.html")

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {
        'form': form
    })
