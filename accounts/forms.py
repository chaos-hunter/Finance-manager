from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']   # include email now
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter new username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
        }
        help_texts = {
            'username': 'Only Letters, digits and @/./+/-/_',
            'email': '',
        }
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address."
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "A user with that email already exists."
            )
        return email
class EmailAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "That username (or email) and password is incorrect."
        ),
        'inactive': _("This account is inactive."),
    }
    username = forms.CharField(label="Username or Email")