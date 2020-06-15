import collections
import json
import time

from django.http import HttpResponseBadRequest, HttpResponse


class RawDict(dict):
    pass


class MobileResponse:
    """
    Class for managing response format for mobile api

    Parameters
    -status
    -errors
    -detail
    """
    ERROR = 'error'
    SUCCESS = 'success'

    def __init__(self):
        self.raw = RawDict()
        self.raw['status'] = self.ERROR
        self.raw['errors'] = []
        self.raw['detail'] = ''
        self.raw['time'] = time.monotonic()

    def add_error(self, parameter, detail):
        self.raw['errors'] = detail

    def set_response(self, dict):
        self.raw['detail'] = dict

    def with_error(self, parameter, detail):
        self.raw['errors'].append({'parameter': parameter, 'detail': detail})
        self.raw['time'] = time.monotonic() - self.raw['time']
        self.raw.pop('detail')
        return json.dumps(self.raw)

    def return_error(self):
        """
        status: error
        errors: []
        :return json raw:
        """
        self.raw.pop('detail')
        self.raw['time'] = time.monotonic() - self.raw['time']
        return json.dumps(self.raw)

    def return_success(self):
        """
        status: success
        detail: []
        :return json raw:
        """
        self.raw['status'] = self.SUCCESS
        self.raw['time'] = time.monotonic() - self.raw['time']
        self.raw.pop('errors')
        return json.dumps(self.raw)


def mobile_400(raw):
    """
    Function for dumps RawDict and return it in HttpResponseBadRequest

    :param raw:
    :return HttpResponseBadRequest:
    """

    return HttpResponseBadRequest(raw, content_type="application/json")


def mobile_200(raw):
    """
    Function for dumps RawDict and return it in HttpResponse

    :param raw:
    :return HttpResponse:
    """
    return HttpResponse(raw, content_type="application/json")


def p(t):
    """Short name for print function"""
    print(t)


def to_dict_list(objects):
    """
    Return dict with all objects also in json

    :param objects: object should define to_dict method
    :return: list of to_dict on each object
    """
    res = []
    if isinstance(objects, collections.Iterable):
        for object in objects:
            try:
                res.append(object.to_dict())
            except Exception as e:
                print('Error in to_dict_list %s WITH %s' % (e, type(e)))
    elif objects:
        res.append(objects.to_dict())

    return res
