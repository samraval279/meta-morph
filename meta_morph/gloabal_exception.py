from rest_framework.views import exception_handler
from rest_framework.response import Response

import traceback
import sys

from meta_morph.global_resposne import ResponseInfo


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first, 
    response = exception_handler(exc, context)
    # print(dir(response))
    handlers = {
        'ValidationError': _handle_generic_error,
        'Http404': _handle_http_error,
        'PermissionDenied': _permission_denied,
        'RestrictedError':_handle_restricted_error 
    }

    exception_class = exc.__class__.__name__

    # print(traceback.format_exc())
    # print(sys.exc_info())
    # print('\n\n')
    # print(exception_class)
    # print('\n\n')

    if exception_class in handlers:
     
        return handlers[exception_class](exc, context, response)
    return response

def _handle_generic_error(exc, context, response):
  
    res = ResponseInfo(response.data, "Fail", False, 400)
    return Response(res.default_errors_payload())

def _permission_denied(exc, context, response):

    res = ResponseInfo(response.data, "You do not have permission to perform this action", False, 403)
    return Response(res.custom_success_payload())

def _handle_http_error(exc, context, response):
  
    res = ResponseInfo(response.data, "Data does not exist for given parameter", False, 404)
    return Response(res.custom_success_payload())

def _handle_restricted_error(exc, context, response):
  
    res = ResponseInfo({}, "you can't perform delete beacuse reference records exist. try to update it", False, 403)
    return Response(res.custom_success_payload())