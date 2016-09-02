from urlparse import urljoin

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException

from requests import get

from django.http import HttpResponse

import ome_seadragon_gateway.settings as gws

import logging
logger = logging.getLogger('ome_seadragon_gw')


def _get_static_content(url):
    response = get(url)
    if response.status_code == status.HTTP_200_OK:
        return HttpResponse(
            response.content, status=status.HTTP_200_OK,
            content_type=response.headers.get('content-type')
        )
    else:
        logger.error('ERROR %s', response.status_code)
        raise APIException()


@api_view()
def get_javascript_min_resource(request, resource_name):
    uri = urljoin(
        gws.OME_SEADRAGON_STATIC_FILES_URL,
        'js/%s.min.js' % resource_name
    )
    return _get_static_content(uri)


@api_view()
def get_css_min_resource(request, resource_name):
    uri = urljoin(
        gws.OME_SEADRAGON_STATIC_FILES_URL,
        'css/%s.min.css' % resource_name
    )
    return _get_static_content(uri)


@api_view()
def get_openseadragon_imgs(request, image_file):
    uri = urljoin(
        gws.OME_SEADRAGON_STATIC_FILES_URL,
        'img/openseadragon/%s' % image_file
    )
    return _get_static_content(uri)
