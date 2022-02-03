"""pdm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include,path

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('api/authentication/', include('pdm.apps.authentication.urls')),
    path('api/demographics/', include('pdm.apps.demographics.urls')),
    path('api/farmers/', include('pdm.apps.farmers.urls')),
    path('api/production-storage-processing-marketing/', include('pdm.apps.production_storage_processing_marketing.urls')),
    path('api/financial-inclusion/', include('pdm.apps.financial_inclusion.urls')),
    path('api/mindset-change/', include('pdm.apps.mindset_change.urls')),
]

if settings.DEBUG:  # add this part at the buttom of the urls.py
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
