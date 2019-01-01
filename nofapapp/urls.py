from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    url('', include('coreapp.urls')),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
]