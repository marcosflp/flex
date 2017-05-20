from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from core.views import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
]
