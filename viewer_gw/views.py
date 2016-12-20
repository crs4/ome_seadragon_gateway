from lxml import etree
from cStringIO import StringIO
from PIL import Image

from rest_framework import status
from rest_framework.exceptions import NotAuthenticated

from django.http import HttpResponse

from ome_seadragon_cache import CacheDriverFactory

import ome_seadragon_gateway.settings as gws
from ome_seadragon_gateway.decorators import ome_session_required
from view_templates.views import SimpleGetWrapper

import logging
logger = logging.getLogger('ome_seadragon_gw')


class DZIWrapper(SimpleGetWrapper):

    @ome_session_required
    def get(self, request, client, image_id, format=None):
        url = self._get_ome_seadragon_url('deepzoom/get/%s.dzi' % image_id)
        response = client.get(url, headers={'X-Requested-With': 'XMLHttpRequest'})
        if response.status_code == status.HTTP_200_OK:
            xml_content = response.content
            tile_size = etree.fromstring(xml_content).get('TileSize')
            request.session.setdefault('images_conf', {}).update({image_id: {'tile_size': tile_size}})
            return HttpResponse(
                xml_content, status=status.HTTP_200_OK,
                content_type=response.headers.get('content-type')
            )
        else:
            logger.error('ERROR CODE: %s', response.status_code)
            raise NotAuthenticated()


class TileWrapper(SimpleGetWrapper):
    permission_classes = ()

    def _tile_from_cache(self, image_id, level, column, row, image_format, tile_size):
        if tile_size:
            cache_settings = gws.CACHE_SETTINGS
            cache = CacheDriverFactory(cache_settings['driver']).get_cache(
                cache_settings['host'], cache_settings['port'], cache_settings['db'],
                cache_settings['expire_time']
            )
            return cache.tile_from_cache(image_id=image_id, level=level, column=column, row=row,
                                         image_format=image_format, tile_size=tile_size)
        else:
            return None

    def _tile_to_cache(self, image_id, level, column, row, image_format, tile_size, tile):
        if tile_size:
            cache_settings = gws.CACHE_SETTINGS
            cache = CacheDriverFactory(cache_settings['driver']).get_cache(
                cache_settings['host'], cache_settings['port'], cache_settings['db'],
                cache_settings['expire_time']
            )
            cache.tile_to_cache(image_id=image_id, level=level, column=column, row=row,
                                image_format=image_format, image_obj=tile, tile_size=tile_size)
        else:
            logger.warn('No configuration for image %s, tiles not saved to cache', image_id)

    def _get_tile_size(self, request, client, image_id):
        if request.session.get('images_conf') and request.session.get('images_conf').get(image_id):
            return request.session.get('images_conf').get(image_id)
        else:
            url = self._get_ome_seadragon_url('deepzoom/get/%s.dzi' % image_id)
            response = client.get(url, headers={'X-Requested-With': 'XMLHttpRequest'})
            if response.status_code == status.HTTP_200_OK:
                xml_content = response.content
                tile_size = etree.fromstring(xml_content).get('TileSize')
                request.session.setdefault('images_conf', {}).update({image_id: {'tile_size': tile_size}})
                return tile_size
            else:
                return None

    @ome_session_required
    def get(self, request, client, image_id, level, column, row, image_format, format=None):
        tile_size = self._get_tile_size(request, client, image_id)
        tile = self._tile_from_cache(image_id, level, column, row, image_format, tile_size)
        if tile is None:
            url = self._get_ome_seadragon_url('deepzoom/get/%s_files/%s/%s_%s.%s' %
                                              (image_id, level, column, row, image_format))
            response = client.get(url, headers={'X-Requested-With': 'XMLHttpRequest'})
            tile = Image.open(StringIO(response.content))
            self._tile_to_cache(image_id, level, column, row, image_format, tile_size, tile)
            if response.status_code == status.HTTP_200_OK:
                return HttpResponse(
                    response.content, status=status.HTTP_200_OK,
                    content_type=response.headers.get('content-type'))
            else:
                logger.error('ERROR CODE: %s', response.status_code)
                raise NotAuthenticated()
        else:
            response = HttpResponse(content_type='image/%s' % image_format)
            tile.save(response, image_format)
            return response


class ImageMppWrapper(SimpleGetWrapper):

    @ome_session_required
    def get(self, request, client, image_id, format=None):
        url = self._get_ome_seadragon_url('deepzoom/image_mpp/%s.dzi' % image_id)
        return self._get(client, url)


class ThumbnailWrapper(SimpleGetWrapper):

    def _thumbnail_from_cache(self, image_id, image_size, image_format):
        cache_settings = gws.CACHE_SETTINGS
        cache = CacheDriverFactory(cache_settings['driver']).get_cache(
            cache_settings['host'], cache_settings['port'], cache_settings['db'],
            cache_settings['expire_time']
        )
        return cache.thumbnail_from_cache(image_id, image_size, image_format)

    def _thumbnail_to_cache(self, image_id, thumbnail, image_size, image_format):
        cache_settings = gws.CACHE_SETTINGS
        cache = CacheDriverFactory(cache_settings['driver']).get_cache(
            cache_settings['host'], cache_settings['port'], cache_settings['db'],
            cache_settings['expire_time']
        )
        cache.thumbnail_to_cache(image_id, thumbnail, image_size, image_format)

    @ome_session_required
    def get(self, request, client, image_id, size, image_format, format=None):
        thumbnail = self._thumbnail_from_cache(image_id, size, image_format)
        if thumbnail is None:
            url = self._get_ome_seadragon_url('deepzoom/get/thumbnail/%s.dzi' % image_id)
            params = {'size': size}
            response = client.get(url, params=params,
                                  headers={'X-Requested-With': 'XMLHttpRequest'})
            thumbnail = Image.open(StringIO(response.content))
            self._thumbnail_to_cache(image_id, thumbnail, size, image_format)
            if response.status_code == status.HTTP_200_OK:
                return HttpResponse(
                    response.content, status=status.HTTP_200_OK,
                    content_type=response.headers.get('content-type')
                )
            else:
                logger.error('ERROR CODE: %s', response.status_code)
                raise NotAuthenticated()
        else:
            response = HttpResponse(content_type='image/%s' % image_format)
            thumbnail.save(response, image_format)
            return response
