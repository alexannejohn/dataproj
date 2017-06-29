"""dataproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from students.viewsets import StudentViewSet
from rest_framework import routers
from students import views
from django.contrib.auth import views as auth_views

from django.views.generic.base import RedirectView
from django.conf import settings

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', StudentViewSet)

admin.site.site_title = 'CEIH student database'
admin.site.index_title = 'Admin'

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'students/login.html'}),
    url(r'^logout/$', auth_views.logout, ),
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^filters/', views.get_filter_options, name='filters'), #Get filters
    url(r'^filterstudents/', views.filter_students, name='filterstudents'), #send filter json, get list of students
    url(r'^enrollprogramtype/', views.filter_enroll_program_type, name='enrollprogramtype'), #filter possible programs due to type, etc
    url(r'^filterspecialization/', views.filter_specialization, name='filterspecialization'), #filter possible specializations due to subject, etc
    url(r'^downloadcsv/', views.csv_view, name='csv_view'), #download csv of students
    url(r'^studentdetail/', views.student_detail, name='student_detail'), #get detailed info on one student
    url(r'^enrollcsv/', views.enroll_csv, name='enroll_csv'), #download csv of enrollments
    url(r'^gradcsv/', views.grad_csv, name='grad_csv'), #download csv of graduations
    url(r'^savesearch/', views.save_search, name='save_search'), # save a search
    url(r'^deletesearch/', views.delete_search, name='delete_search'), # delete a search
    url(r'^getsearches/', views.get_searches, name='get_searches'),  # get all searches
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),  # favicon redirect
]
