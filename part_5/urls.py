from django.conf.urls import url, include
from . import views

app_name = 'part_5'

urlpatterns = [
    url(r'^$', views.simple_upload2, name = 'form_upload2')
]
