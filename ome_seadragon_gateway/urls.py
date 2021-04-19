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
from django.urls import path, re_path
from django.conf.urls import include
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns

from viewer_gw.views import DZIWrapper, JSONWrapper, JSONMetadataWrapper, TileWrapper, \
    ImageMppWrapper, ThumbnailWrapper
from ome_data_gw.views import ProjectsListWrapper, ProjectDetailsWrapper, DatasetDetailsWrapper, \
    ImagesQuickListWrapper, ImageDetailsWrapper
from ome_tags_gw.views import AnnotationsWrapper, TagsetDetailsWrapper, TagDetailsWrapper
from static_files_gw.views import get_javascript_min_resource, get_css_min_resource, get_openseadragon_imgs
from examples.views import get_example_viewer

urlpatterns = {
    # DZI files
    re_path('api/deepzoom/(?P<image_id>[0-9]+).dzi/', DZIWrapper.as_view({'get': 'get'})),
    re_path('api/deepzoom/(?P<image_id>[0-9]+).json/', JSONWrapper.as_view({'get': 'get'})),

    # tiles
    re_path(r'api/deepzoom/(?P<image_id>[0-9]+)_files/<int:level>/<int:column> <int:row>.(?P<image_format>[\w]+)$',
            TileWrapper.as_view({'get': 'get'})),

    # image microns per pixel
    re_path('api/image_mpp/(?P<image_id>[0-9]+)/', ImageMppWrapper.as_view({'get': 'get'})),

    # image mpp + tile sources
    re_path('api/deepzoom/(?P<image_id>[0-9]+)_metadata.json/', JSONMetadataWrapper.as_view({'get': 'get'})),

    # thumbnails
    re_path('api/thumbnail/(?P<image_id>[0-9]+)/(?P<size>[0-9]+)/(?P<image_format>jpeg|png)/',
            ThumbnailWrapper.as_view({'get': 'get'})),

    # projects, datasets and images details
    path('api/projects/', ProjectsListWrapper.as_view({'get': 'get'})),
    path('api/projects/datasets/', ProjectsListWrapper.as_view({'get': 'get_with_datasets'})),
    re_path('api/projects/(?P<project_id>[0-9]+)/', ProjectDetailsWrapper.as_view({'get': 'get'})),
    re_path('api/projects/(?P<project_id>[0-9]+)/datasets/',
            ProjectDetailsWrapper.as_view({'get': 'get_with_datasets'})),
    re_path('api/projects/(?P<project_id>[0-9]+)/datasets/images/',
            ProjectDetailsWrapper.as_view({'get': 'get_with_images'})),
    re_path('api/projects/(?P<project_id>[0-9]+)/datasets/images/full_series/',
            ProjectDetailsWrapper.as_view({'get': 'get_with_full_series'})),

    re_path(r'api/datasets/(?P<dataset_id>[0-9]+)/', DatasetDetailsWrapper.as_view({'get': 'get'})),
    re_path(r'api/datasets/(?P<dataset_id>[0-9]+)/images/', DatasetDetailsWrapper.as_view({'get': 'get_with_images'})),
    re_path(r'api/datasets/(?P<dataset_id>[0-9]+)/images/full_series/',
         DatasetDetailsWrapper.as_view({'get': 'get_with_full_series'})),

    re_path(r'api/images/', ImagesQuickListWrapper.as_view({'get': 'get'})),
    re_path(r'api/images/full_series/',
         ImagesQuickListWrapper.as_view({'get': 'get_with_full_series'})),
    re_path(r'api/images/(?P<image_id>[0-9]+)/',
         ImageDetailsWrapper.as_view({'get': 'get'})),
    re_path(r'api/images/(?P<image_id>[0-9]+)/rois/',
         ImageDetailsWrapper.as_view({'get': 'get_with_rois'})),

    # TAGs
    path(r'api/annotations/', AnnotationsWrapper.as_view({'get': 'get'})),
    path(r'api/annotations/images/', AnnotationsWrapper.as_view({'get': 'get_with_images'})),
    re_path(r'api/annotations/(?P<query>[\w\-.]+)/$', AnnotationsWrapper.as_view({'get': 'find'})),
    re_path(r'api/annotations/(?P<query>[\w\-.]+)/images/$', AnnotationsWrapper.as_view({'get': 'find_with_images'})),
    re_path(r'api/tagsets/(?P<tagset_id>[0-9]+)/', TagsetDetailsWrapper.as_view({'get': 'get'})),
    re_path(r'api/tagsets/(?P<tagset_id>[0-9]+)/tags/', TagsetDetailsWrapper.as_view({'get': 'get_with_tags'})),
    re_path(r'api/tagsets/(?P<tagset_id>[0-9]+)/tags/images/$', TagsetDetailsWrapper.as_view({'get': 'get_with_images'})),
    re_path(r'api/tags/(?P<tag_id>[0-9]+)/$', TagDetailsWrapper.as_view({'get': 'get'})),
    re_path(r'api/tags/(?P<tag_id>[0-9]+)/images/$', TagDetailsWrapper.as_view({'get': 'get_with_images'})),

    # ome_seadragon static files
    re_path('static/ome_seadragon/js/'
            r'(?P<resource_name>ome_seadragon|jquery|openseadragon|openseadragon\-scalebar|paper\-full|bootstrap).min.js$',
            get_javascript_min_resource),
    re_path('static/ome_seadragon/css/(?P<resource_name>bootstrap).min.css$', get_css_min_resource),
    re_path(r'static/ome_seadragon/img/openseadragon/(?P<image_file>[\w\-.]+)$', get_openseadragon_imgs),

    # examples
    re_path('examples/viewer/(?P<image_id>[0-9]+)/', get_example_viewer),

    # admin
    path('admin/', admin.site.urls),

    # OAuth2Autentication admin
    path('oauth2/', include('oauth2_provider.urls', namespace='oauth2')),
}

urlpatterns = format_suffix_patterns(urlpatterns)
