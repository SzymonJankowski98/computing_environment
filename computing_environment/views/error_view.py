from django.shortcuts import render

def error_403(request, *args, **argv):
    response = render(request, 'errors/error403.html')
    response.status_code = 403
    return response

def error_404(request, *args, **argv):
    response = render(request, 'errors/error404.html')
    response.status_code = 404
    return response

def error_500(request, *args, **argv):
    response = render(request, 'errors/error500.html')
    response.status_code = 500
    return response
