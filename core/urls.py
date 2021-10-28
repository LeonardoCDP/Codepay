from django.urls import path

from core import views as v

app_name = 'core'


urlpatterns = [
    path(r'/', v.index, name='index'),
    path(r'rpa/', v.rpa, name='rpa'),
    path(r'rpa_adm/', v.rpa_adm, name='rpa_adm'),
]
