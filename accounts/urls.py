from django.urls import path, include
from .views import SignUpView, activate_account, profile
from .forms import EmailAuthenticationForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),

    # 1) Your custom login, using your EmailAuthenticationForm:
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html',
            authentication_form=EmailAuthenticationForm
        ),
        name='login'
    ),

    # 2) Logout & profile
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),

    # 3) All the other auth routes (password reset/change, etc.)
    path('', include('django.contrib.auth.urls')),
]
