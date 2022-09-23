from django.http import HttpResponse


def bad_request():
    return HttpResponse(content='Bad request', status=400)
