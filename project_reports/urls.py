from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^own/$', views.consolidated_report, name='own_projects_report'),
    url(r'^all/$', views.consolidated_report, name='all_projects_report'),
    url(r'^all/(?P<category>\w+)/$', views.consolidated_report, name='projects_report'),
]
