from django.shortcuts import render


def get_example_viewer(request, image_id):
    base_url = '%s://%s' % (request.META['wsgi.url_scheme'], request.META['HTTP_HOST'])
    return render(request, 'examples/viewer.html',
                  {'image_id': image_id, 'host_name': base_url, 'mirax': False})
