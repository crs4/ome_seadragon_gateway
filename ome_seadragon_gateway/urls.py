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

from viewer_gw.views import DZIWrapper, TileWrapper, ImageMppWrapper
from ome_data_gw.views import ProjectsListWrapper, ProjectDetailsWrapper, DatasetDetailsWrapper,\
    ImagesQuickListWrapper, ImageDetailsWrapper
from static_files_gw.views import get_javascript_min_resource, get_css_min_resource, get_openseadragon_imgs
from examples.views import get_example_viewer

urlpatterns = [
    # DZI files
    url(r'^api/deepzoom/(?P<image_id>[0-9]+)/$',
        DZIWrapper.as_view({'get': 'get'})),

    # tiles
    url(r'^api/deepzoom/(?P<image_id>[0-9]+)_files/(?P<level>[0-9]+)/'
        r'(?P<column>[0-9]+)_(?P<row>[0-9]+).(?P<image_format>[\w]+)$',
        TileWrapper.as_view({'get': 'get'})),

    # image microns per pixel
    url(r'^api/image_mpp/(?P<image_id>[0-9]+)/$',
        ImageMppWrapper.as_view({'get': 'get'})),

    # projects, datasets and images details
    url(r'api/projects/$', ProjectsListWrapper.as_view({'get': 'get'})),
    url(r'api/projects/datasets/$',
        ProjectsListWrapper.as_view({'get': 'get_with_datasets'})),
    url(r'api/projects/(?P<project_id>[0-9]+)/$',
        ProjectDetailsWrapper.as_view({'get': 'get'})),
    url(r'api/projects/(?P<project_id>[0-9]+)/datasets/$',
        ProjectDetailsWrapper.as_view({'get': 'get_with_datasets'})),
    url(r'api/projects/(?P<project_id>[0-9]+)/datasets/images/$',
        ProjectDetailsWrapper.as_view({'get': 'get_with_images'})),
    url(r'api/projects/(?P<project_id>[0-9]+)/datasets/images/full_series/$',
        ProjectDetailsWrapper.as_view({'get': 'get_with_full_series'})),
    url(r'api/datasets/(?P<dataset_id>[0-9]+)/$',
        DatasetDetailsWrapper.as_view({'get': 'get'})),
    url(r'api/datasets/(?P<dataset_id>[0-9]+)/images/$',
        DatasetDetailsWrapper.as_view({'get': 'get_with_images'})),
    url(r'api/datasets/(?P<dataset_id>[0-9]+)/images/full_series/$',
        DatasetDetailsWrapper.as_view({'get': 'get_with_full_series'})),
    url(r'api/images/$', ImagesQuickListWrapper.as_view({'get': 'get'})),
    url(r'api/images/full_series/$',
        ImagesQuickListWrapper.as_view({'get': 'get_with_full_series'})),
    url(r'api/images/(?P<image_id>[0-9]+)/$',
        ImageDetailsWrapper.as_view({'get': 'get'})),
    url(r'api/images/(?P<image_id>[0-9]+)/rois/$',
        ImageDetailsWrapper.as_view({'get': 'get_with_rois'})),

    # ome_seadragon static files
    url(r'^gw/static/js/(?P<resource_name>ome_seadragon|jquery|openseadragon|openseadragon\-scalebar|paper\-full|bootstrap).min.js$',
        get_javascript_min_resource),
    url(r'^gw/static/css/(?P<resource_name>bootstrap).min.css$', get_css_min_resource),
    url(r'^gw/static/img/openseadragon/(?P<image_file>[\w\-.]+)$', get_openseadragon_imgs),

    # examples
    url(r'^examples/viewer/(?P<image_id>[0-9]+)/$', get_example_viewer),

    # admin
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
