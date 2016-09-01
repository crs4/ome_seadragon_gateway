from view_templates.views import SimpleGetWrapper

from ome_seadragon_gateway.decorators import ome_session_required

import logging
logger = logging.getLogger('ome_seadragon_gw')


class ProjectsListWrapper(SimpleGetWrapper):

    @ome_session_required
    def get(self, request, client, format=None):
        url = self._get_ome_seadragon_url('get/projects/')
        return self._get(client, url)


class ProjectDetailsWrapper(SimpleGetWrapper):

    @ome_session_required
    def get(self, request, client, project_id, format=None):
        url = self._get_ome_seadragon_url('get/project/%s/' % project_id)
        return self._get(client, url)

    @ome_session_required
    def get_with_datasets(self, request, client, project_id, format=None):
        url = self._get_ome_seadragon_url('get/project/%s/' % project_id)
        params = {'datasets': 'true'}
        return self._get(client, url, params)

    @ome_session_required
    def get_with_images(self, request, client, project_id, format=None):
        url = self._get_ome_seadragon_url('get/project/%s/' % project_id)
        params = {'datasets': 'true', 'image': 'true'}
        return self._get(client, url, params)

    @ome_session_required
    def get_with_full_series(self, request, client, project_id, format=None):
        url = self._get_ome_seadragon_url('get/project/%s/' % project_id)
        params = {'datasets': 'true', 'image': 'true', 'full_series': 'true'}
        return self._get(client, url, params)


class DatasetDetailsWrapper(SimpleGetWrapper):

    @ome_session_required
    def get(self, request, client, dataset_id, format=None):
        url = self._get_ome_seadragon_url('get/datasets/%s/' % dataset_id)
        return self._get(client, url)

    @ome_session_required
    def get_with_images(self, request, client, dataset_id, format=None):
        url = self._get_ome_seadragon_url('get/datasets/%s/' % dataset_id)
        params = {'images': 'true'}
        return self._get(client, url, params)

    @ome_session_required
    def get_with_full_series(self, request, client, datset_id, format=None):
        url = self._get_ome_seadragon_url('get/datasets/%s/' % dataset_id)
        params = {'images': 'true', 'full_series': 'true'}
        return self._get(client, url, params)


class ImageDetailsWrapper(SimpleGetWrapper):

    @ome_session_required
    def get(self, request, client, image_id, format=None):
        url = self._get_ome_seadragon_url('get/image/%s/' % image_id)
        return self._get(client, url)

    @ome_session_required
    def get_with_rois(self, request, client, image_id, format=None):
        url = self._get_ome_seadragon_url('get/image/%s/' % image_id)
        params = {'rois': 'true'}
        return self._get(client, url, params)


class ImagesQuickListWrapper(SimpleGetWrapper):

    @ome_session_required
    def get(self, request, client, format=None):
        url = self._get_ome_seadragon_url('get/images/index/')
        return self._get(client, url)

    @ome_session_required
    def get_with_full_series(self, request, client, format=None):
        url = self._get_ome_seadragon_url('get/images/index/')
        params = {'full_series': 'true'}
        return self._get(client, url, params)
