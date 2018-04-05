from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.view_report, name='view_report'),	
	url(r'^edit/(?P<field_type>\d+)/$', views.edit_report_field, name='edit_report_field'),
	url(r'^generate/$', views.generate_report, name='generate_project_report'),
]