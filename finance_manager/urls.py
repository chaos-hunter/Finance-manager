from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),

    # make sure this line is present:
    path('accounts/', include('accounts.urls')),

    # ...and don’t forget the auth URLs if you’re using built-in views:
    path('accounts/', include('django.contrib.auth.urls')),

    path('wallets/', include('wallets.urls')),
    path('',        RedirectView.as_view(url='/wallets/')),
]
