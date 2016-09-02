from view_templates.views import SimpleGetWrapper

from ome_seadragon_gateway.decorators import ome_session_required

import logging
logger = logging.getLogger('ome_seadragon_gw')


class AnnotationsWrapper(SimpleGetWrapper):

    @ome_session_required
    def get(self, request, client, format=None):
        url = self._get_ome_seadragon_url('get/annotations/')
        return self._get(client, url)

    @ome_session_required
    def get_with_images(self, request, client, format=None):
        url = self._get_ome_seadragon_url('get/annotations/')
        params = {'fetch_imgs': 'true'}
        return self._get(client, url, params)

    @ome_session_required
    def find(self, request, client, query, format=None):
        url = self._get_ome_seadragon_url('find/annotations/')
        params = {'query': query}
        return self._get(client, url, params)

    @ome_session_required
    def find_with_images(self, request, client, query, format=None):
        url = self._get_ome_seadragon_url('find/annotations/')
        params = {'query': query, 'fetch_imgs': 'true'}
        return self._get(client, url, params)


class TagsetDetailsWrapper(SimpleGetWrapper):

    @ome_session_required
    def get(self, request, client, tagset_id, format=None):
        url = self._get_ome_seadragon_url('get/tagset/%s/' % tagset_id)
        return self._get(client, url)

    @ome_session_required
    def get_with_tags(self, request, client, tagset_id, format=None):
        url = self._get_ome_seadragon_url('get/tagset/%s/' % tagset_id)
        params = {'tags': 'true'}
        return self._get(client, url, params)

    @ome_session_required
    def get_with_images(self, request, client, tagset_id, format=None):
        url = self._get_ome_seadragon_url('get/tagset/%s/' % tagset_id)
        params = {'tags': 'true', 'images': 'true'}
        return self._get(client, url, params)


class TagDetailsWrapper(SimpleGetWrapper):

    @ome_session_required
    def get(self, request, client, tag_id, format=None):
        url = self._get_ome_seadragon_url('get/tag/%s/' % tag_id)
        return self._get(client, url)

    @ome_session_required
    def get_with_images(self, request, client, tag_id, format=None):
        url = self._get_ome_seadragon_url('get/tag/%s/' % tag_id)
        params = {'images': 'true'}
        return self._get(client, url, params)
