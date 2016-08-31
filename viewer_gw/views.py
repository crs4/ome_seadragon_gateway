from urlparse import urljoin

from lxml import etree
from cStringIO import StringIO
from PIL import Image

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotAuthenticated

from django.http import HttpResponse

from ome_seadragon_cache import CacheDriverFactory

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
        logger.info('Payload: %s', uri)
        response = client.get(uri, headers={'X-Requested-With': 'XMLHttpRequest'})
        logger.info('STATUS CODE: %d', response.status_code)
        if response.status_code == status.HTTP_200_OK:
            xml_content = response.content
            tile_size = etree.fromstring(xml_content).get('TileSize')
            request.session.setdefault('images_conf', {}).update({image_id: {'tile_size': tile_size}})
            return HttpResponse(
                xml_content, status=status.HTTP_200_OK,
                content_type=response.headers.get('content-type')
            )
        else:
            logger.error('ERROR')
            raise NotAuthenticated()


class OmeTileWrapper(APIView):

    def _tile_from_cache(self, request, image_id, level, column, row, image_format):
        if request.session.get('images_conf') and request.session.get('images_conf').get(image_id):
            cache_settings = gws.CACHE_SETTINGS
            cache = CacheDriverFactory(cache_settings['driver']).get_cache(
                cache_settings['host'], cache_settings['port'], cache_settings['db'],
                cache_settings['expire_time']
            )
            logger.info('Retrieving tile from cache for image %s (L:%s R:%s C:%s)',
                        image_id, level, row, column)
            return cache.tile_from_cache(image_id=image_id, level=level, column=column, row=row,
                                         image_format=image_format,
                                         tile_size=int(request.session.get('images_conf').get(image_id)['tile_size']))
        else:
            return None

    def _tile_to_cache(self, request, image_id, level, column, row, image_format, tile):
        if request.session.get('images_conf') and request.session.get('images_conf').get(image_id):
            cache_settings = gws.CACHE_SETTINGS
            cache = CacheDriverFactory(cache_settings['driver']).get_cache(
                cache_settings['host'], cache_settings['port'], cache_settings['db'],
                cache_settings['expire_time']
            )
            logger.info('Saving tile to cache for image %s (L:%s R:%s C:%s)',
                        image_id, level, row, column)
            cache.tile_to_cache(image_id=image_id, level=level, column=column, row=row,
                                image_format=image_format, image_obj=tile,
                                tile_size=int(request.session.get('images_conf').get(image_id)['tile_size']))
        else:
            logger.warn('No configuration for image %s, tiles not saved to cache', image_id)

    @ome_session_required
    def get(self, request, client, image_id, level, column, row, image_format, format=None):
        tile = self._tile_from_cache(request, image_id, level, column, row, image_format)
        if tile is None:
            uri = urljoin(
                gws.OME_SEADRAGON_BASE_URL,
                'deepzoom/get/%s_files/%s/%s_%s.%s' % (image_id, level, column, row, image_format)
            )
            logger.info('Payload: %s', uri)
            response = client.get(uri, headers={'X-Requested-With': 'XMLHttpRequest'})
            tile = Image.open(StringIO(response.content))
            self._tile_to_cache(request, image_id, level, column, row, image_format, tile)
            logger.info('STATUS CODE: %d', response.status_code)
            if response.status_code == status.HTTP_200_OK:
                logger.info(response.headers.get('content-type'))
                return HttpResponse(
                    response.content, status=status.HTTP_200_OK,
                    content_type=response.headers.get('content-type'))
            else:
                logger.error('ERROR')
        else:
            response = HttpResponse(content_type='image/%s' % image_format)
            tile.save(response, image_format)
            return response


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
