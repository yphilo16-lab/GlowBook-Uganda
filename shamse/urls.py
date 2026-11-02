from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap

"""
URL configuration for shamse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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

urlpatterns = [
    #Django Admin
    path('admin/', admin.site.urls),
    #Google Search Console Verification
    path(
        'googledeed6e53a34f4187.html',
        lambda request: HttpResponse(
            'google-site-verification:googledeed6e53a34f4187.html',
            content_type='text/html'
        )
     ),
    #Main Website URLS
    path('', include('core.urls')),
    #Sitemap URL
    path(
        'sitemap.xml', 
        sitemap, 
        {'sitemaps': {'pages': StaticViewSitemap}}, 
        name='django.contrib.sitemaps.views.sitemap'
        ),
]
