from urlparse import urljoin

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import NotAuthenticated

from oauth2_provider.ext.rest_framework import TokenHasScope

from django.http import HttpResponse

import ome_seadragon_gateway.settings as gws

import logging
logger = logging.getLogger('ome_seadragon_gw')


class SimpleGetWrapper(ViewSet):
    permission_classes = (TokenHasScope, )
    required_scopes = ['read']

    def _get_ome_seadragon_url(self, url):
        return urljoin(
            gws.OME_SEADRAGON_BASE_URL, url
        )

    def _get(self, client, url, params=None):
        logger.debug('_get --- URL: %s --- params: %r', url, params)
        response = client.get(url, params=params,
                              headers={'X-Requested-With': 'XMLHttpRequest'})
        if response.status_code == status.HTTP_200_OK:
            return HttpResponse(
                response.content, status=status.HTTP_200_OK,
                content_type=response.headers.get('content-type')
            )
        else:
            logger.error('ERROR CODE: %s', response.status_code)
            raise NotAuthenticated()
