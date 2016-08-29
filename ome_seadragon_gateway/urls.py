"""ome_seadragon_gateway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns

from viewer_gw.views import OmeDZIWrapper, OmeTileWrapper
from static_files_gw.views import get_javascript_min_resource, get_css_min_resource

urlpatterns = [
    # DZI files
    url(r'api/dzi/(?P<image_id>[0-9]+)/$', OmeDZIWrapper.as_view()),

    # TILES
    url(r'api/tiles/(?P<image_id>[0-9]+)_files/(?P<level>[0-9]+)/'
        r'(?P<column>[0-9]+)_(?P<row>[0-9]+).(?P<image_format>[\w]+)$',
        OmeTileWrapper.as_view()),

    # ome_seadragon static files
    url(r'gw/static/js/(?P<resource_name>ome_seadragon|jquery|openseadragon|openseadragon\-scalebar|paper\-full|bootstrap).min.js$',
        get_javascript_min_resource),
    url(r'^gw/static/css/(?P<resource_name>bootstrap).min.css$', get_css_min_resource),
    url(r'^gw/static/img/openseadragon/(?P<image_file>[\w\-.]+)$', get_openseadragon_imgs),

    # admin
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
