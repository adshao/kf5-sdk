#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Guojian Shao'
__email__ = 'guojian@unitedstack.com; tjusgj@gmail.com'

import urllib
import urllib2
import hashlib
import json
from collections import OrderedDict


class Client(object):

    def __init__(self, domain=None, key=None, api_version='v1'):
        self._domain = domain
        self._key = key
        self._api_version = api_version
        self.url = None
        self.domain = domain

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        self._domain = value
        self.url = 'http://{domain}.kf5.com/api/{api_version}'.format(domain=self._domain,
                                                                      api_version=self._api_version)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    def __getattr__(self, item):
        return self._api_wrapper(item)

    def _api_wrapper(self, api):

        def _call_api(*args, **kwargs):
            if args:
                api_name = args[0]
            else:
                api_name = api.replace('_', '/')

            api_url = '{base_url}/{api}'.format(base_url=self.url,
                                                api=api_name)
            params = OrderedDict(sorted(kwargs.items()))
            s = '&'.join(['{k}={v}'.format(k=k, v=v) for k, v in params.items()])
            if len(s) > 0:
                s += '&'
            s += self.key
            m = hashlib.md5()
            m.update(s)
            sign = m.hexdigest()
            params['sign'] = sign
            try:
                req = urllib2.Request(api_url, urllib.urlencode(params))
                res = urllib2.urlopen(req)
                result = json.loads(res.read())
                if getattr(result, 'err', 0) == 1:
                    raise APIError('API Error', result['msg'])
                return result
            except Exception as e:
                raise APIError('Error', e.message)

        return _call_api


class APIError(Exception):
    def __init__(self, error, message):
        self.error = error
        self.message = message

    def __str__(self):
        return json.dumps(dict(error=self.error, message=self.message))

