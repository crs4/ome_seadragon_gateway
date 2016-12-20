import settings
from requests import Session
from urlparse import urljoin
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

import logging
logger = logging.getLogger('ome_seadragon_gw')


def ome_session_required(function):
    def _dec(view_func):
        def _view(ctx, request, *args, **kwargs):
            client = Session()
            ome_session_id = request.session.get('ome_session_id', None)
            session_valid = False
            if ome_session_id:
                logger.info('Session ID is: %s', ome_session_id)
                client.cookies.set(settings.OMERO_COOKIE_NAME, ome_session_id)
                # check if sessionid points to a valid session
                url = urljoin(settings.OME_SEADRAGON_BASE_URL, 'connect/')
                r = client.get(url, headers={'X-Requested-With': 'XMLHttpRequest'})
                session_valid = (r.status_code == status.HTTP_204_NO_CONTENT)
            if not session_valid:
                # remove sessionid cookie from client, if exists
                try:
                    client.cookies.pop(settings.OMERO_COOKIE_NAME)
                    logger.info('Cleaning existing session ID')
                except KeyError:
                    logger.info('No session ID to clean')
                # open a new connection
                url = urljoin(settings.OME_SEADRAGON_BASE_URL, 'connect/')
                payload = {
                    'username': settings.OME_USER,
                    'password': settings.OME_PASSWD,
                    'server': settings.OME_SERVER_ID
                }
                # act as a ajax request in order to obtain a 403 error if using wrong
                # authentication credentials
                r = client.get(url, params=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
                logger.info(r.url)
                if r.status_code == status.HTTP_204_NO_CONTENT:
                    request.session['ome_session_id'] = client.cookies.get(settings.OMERO_COOKIE_NAME)
                elif r.status_code == status.HTTP_403_FORBIDDEN:
                    raise PermissionDenied()
            return view_func(ctx, request, client, *args, **kwargs)
        return _view
    return _dec(function)
