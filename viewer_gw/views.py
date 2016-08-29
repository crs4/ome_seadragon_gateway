from urlparse import urljoin

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotAuthenticated

from django.http import HttpResponse

import ome_seadragon_gateway.settings as gws
from ome_seadragon_gateway.decorators import ome_session_required

import logging
logger = logging.getLogger('ome_seadragon_gw')


class OmeDZIWrapper(APIView):

    @ome_session_required
    def get(self, request, client, image_id, format=None):
        uri = urljoin(
            gws.OME_SEADRAGON_BASE_URL,
            'deepzoom/get/%s.dzi' % image_id
        )
        logger.info('Paylod: %s', uri)
        response = client.get(uri, headers={'X-Requested-With': 'XMLHttpRequest'})
        logger.info('STATUS CODE: %d', response.status_code)
        if response.status_code == status.HTTP_200_OK:
            return HttpResponse(
                response.content, status=status.HTTP_200_OK,
                content_type=response.headers.get('content-type')
            )
        else:
            logger.error('ERROR')
            raise NotAuthenticated()


class OmeTileWrapper(APIView):

    @ome_session_required
    def get(self, request, client, image_id, level, column, row, image_format, format=None):
        uri = urljoin(
            gws.OME_SEADRAGON_BASE_URL,
            'deepzoom/get/%s_files/%s/%s_%s.%s' % (image_id, level, column, row, image_format)
        )
        logger.info('Payload: %s', uri)
        response = client.get(uri, headers={'X-Requested-With': 'XMLHttpRequest'})
        logger.info('STATUS CODE: %d', response.status_code)
        if response.status_code == status.HTTP_200_OK:
            logger.info(response.headers.get('content-type'))
            return HttpResponse(
                response.content, status=status.HTTP_200_OK,
                content_type=response.headers.get('content-type'))
        else:
            logger.error('ERROR')


class ImageMppWrapper(APIView):

    @ome_session_required
    def get(self, request, client, image_id, format=None):
        uri = urljoin(
            gws.OME_SEADRAGON_BASE_URL,
            'deepzoom/image_mpp/%s.dzi' % image_id
        )
        logger.info('Payload: %s', uri)
        response = client.get(uri, headers={'X-Requested-With': 'XMLHttpRequest'})
        logger.info('STATUS CODE: %d', response.status_code)
        if response.status_code == status.HTTP_200_OK:
            logger.info(response.headers.get('content-type'))
            return HttpResponse(
                response.content, status=status.HTTP_200_OK,
                content_type=response.headers.get('content-type')
            )
        else:
            logger.error('ERROR')
