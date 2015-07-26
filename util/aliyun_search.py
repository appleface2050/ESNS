# -*- coding: utf-8 -*-
"""Python unofficial sdk of aliyun open search.

Email: me@defool.me
"""
from __future__ import absolute_import
import json
import time
import copy
import hashlib
import base64
import hmac
import uuid
from datetime import datetime
from operator import itemgetter
import requests

try:
    from urllib.parse import urlencode, quote  # py 3.x
except ImportError:
    from urllib import urlencode, quote  # py 2.x


class SearchClient(object):

    qps_limit = 200  # max number of calls per second. set 0 if unlimit
    qps_offset = 0
    last_query_time = 0

    def __init__(self, key, secret):
        version = 'v2'
        self.base_url = 'http://opensearch-cn-beijing.aliyuncs.com'
        self.sign_params = {
            'Version': version,
            'AccessKeyId': key,
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureVersion': '1.0',
        }
        self.secret = secret
        self.session = requests.session()

    def call(self, path, params={}, method='GET'):
        if SearchClient.qps_limit > 0:
            if SearchClient.qps_offset == SearchClient.qps_limit:
                t = int(time.time())
                if t == SearchClient.last_query_time:  # wait a second
                    time.sleep(1)
                SearchClient.last_query_time = t
            SearchClient.qps_offset = (
                SearchClient.qps_offset + 1) % (SearchClient.qps_limit + 1)

        params.update(self.sign_params)
        now = datetime.utcnow()
        params['Timestamp'] = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        params['SignatureNonce'] = self.__nonce()
        params['Signature'] = self.__sign(params, method)

        url = self.base_url + path
        if method == 'GET':
            # res = self.session.get(url + '?' + urlencode(params))
            #print url + '?' + urlencode(params)
            return url + '?' + urlencode(params)
        else:
            # res = self.session.post(url, params)
            return url + '?' + urlencode(params)
        # assert res.status_code == 200
        # return json.loads(res.text)


    def call_result(self, path, params={}, method='GET'):
        if SearchClient.qps_limit > 0:
            if SearchClient.qps_offset == SearchClient.qps_limit:
                t = int(time.time())
                if t == SearchClient.last_query_time:  # wait a second
                    time.sleep(1)
                SearchClient.last_query_time = t
            SearchClient.qps_offset = (
                SearchClient.qps_offset + 1) % (SearchClient.qps_limit + 1)

        params.update(self.sign_params)
        now = datetime.utcnow()
        params['Timestamp'] = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        params['SignatureNonce'] = self.__nonce()
        params['Signature'] = self.__sign(params, method)

        url = self.base_url + path
        if method == 'GET':
            res = self.session.get(url + '?' + urlencode(params))
            # #print url + '?' + urlencode(params)
            # return url + '?' + urlencode(params)
        else:
            res = self.session.post(url, params)
            # return url + '?' + urlencode(params)
        assert res.status_code == 200
        return json.loads(res.text)


    def __sign(self, params={}, method='GET'):
        if 'sign_mode' in params and params['sign_mode'] == 1:
            params = copy.copy(params)
            del params['items']

        query = '&'.join(self.__percent_encode(k) + '=' + self.__percent_encode(v)
                         for k, v in sorted(params.items(), key=itemgetter(0)))
        base_string = method.upper() + '&%2F&' + self.__percent_encode(query)
        b64string = base64.b64encode(
            hmac.new(self.secret + '&', base_string, hashlib.sha1).digest())
        return b64string

    def __percent_encode(self, string):
        return quote(str(string)).replace('+', '%20').replace('*', '%%2A').replace('%%7E', '~')

    def __nonce(self):
        return str(uuid.uuid4())


class SearchIndex(object):

    def __init__(self, index_name, client):
        self.client = client
        self.index_name = index_name
        self.path = '/index/' + index_name

    def create(self, template):
        return self.client.call(self.path, {'action': 'create', 'template': template})

    def delete(self):
        return self.client.call(self.path, {'action': 'delete'})

    def status(self):
        return self.client.call(self.path, {'action': 'status'})

    def index(self):
        return self.client.call('/index/')


class SearchDoc(object):

    def __init__(self, index_name, client):
        self.client = client
        self.index_name = index_name
        self.path = '/index/doc/' + index_name
        self.search_path = '/search'

    def add(self, doc, table_name):
        return self.action('add', doc, table_name)

    def delete(self, docid, table_name):
        if type(docid) == list:
            docs = [{'id': d} for d in docid]
        else:
            docs = [{'id': docid}]
        return self.action('delete', docs, table_name)

    def update(self, doc, table_name):
        return self.action('add', doc, table_name)

    def detail(self, docid, table_name):
        params = {
            'id': docid,
            'table_name': table_name,
        }
        return self.client.call(self.path, params, method='POST')

    def action(self, cmd, docs, table_name):
        if type(docs) == dict:
            docs = [{'cmd': cmd, 'fields': docs}]
        else:
            docs = [{'cmd': cmd, 'fields': d} for d in docs]

        params = {
            'action': 'push',
            'items': json.dumps(docs),
            'table_name': table_name,
            'sign_mode': 1,
        }
        return self.client.call(self.path, params, method='POST')

    def search(self, query, index_name=None, fetch_fields=None, formula_name=None, first_formula_name=None, summary=None, result=True):
        params = {'index_name': index_name or self.index_name, 'query': query}
        if fetch_fields is not None:
            params['fetch_fields'] = fetch_fields
        if formula_name is not None:
            params['formula_name'] = formula_name
        if first_formula_name is not None:
            params['first_formula_name'] = first_formula_name
        if summary is not None:
            params['summary'] = summary
        if result:
            return self.client.call_result(self.search_path, params, method='GET')
        else:
            return self.client.call(self.search_path, params, method='GET')


class AliyunSearch(object):
    """
    阿里云开放搜索
    by：尚宗凯 at：2015-05-14
    """
    def __init__(self,index_name,table_name):
        self.key = 'XAD7Ua8QOPafVICv'
        self.secret = 'Eo3oFX9iLQi6nIsLCYMkQoq5ItBj3V'
        # self.index_name = 'project'
        # self.table_name = 'project'
        self.index_name = index_name
        self.table_name = table_name
        self.client = SearchClient(self.key, self.secret)

    def generate_query_url(self, query="", result=False):
        self.doc = SearchDoc(self.index_name, self.client)
        return self.doc.search('query=default:"%s"'%query)

    def make_query(self, query):
        self.doc = SearchDoc(self.index_name, self.client)
        return self.doc.search('query=default:"%s"'% query)

    @classmethod
    def query(cls, index_name, table_name, query=""):
        return cls(index_name,table_name).make_query(query)


if __name__ == '__main__':
    # from __future__ import print_function
    # import time


    # key = 'XAD7Ua8QOPafVICv'
    # secret = 'Eo3oFX9iLQi6nIsLCYMkQoq5ItBj3V'
    # index_name = 'project'
    # table_name = 'project'
    #
    # client = SearchClient(key, secret)
    # doc = SearchDoc(index_name, client)
    # print('search result:', doc.search('query=default:"科技大厦"'))

    # s = AliyunSearch()
    # # url = s.generate_query_url("科技")
    # # print url
    # print s.query("科技")
    print AliyunSearch.query(index_name="project", table_name="project", query="科技大厦")



    # index = SearchIndex(index_name, client)

    # print('app list:', index.index())
    #

    #
    # items = [
    #     {
    #         "id": "12113313177",
    #         "title": "A test title 1",
    #         "content": "搜索， 内容",
    #     },
    #     {
    #         "id": "12113933131",
    #         "title": "A test Title 2",
    #         "content": "搜索， 内容2"
    #     }
    # ]
    # item = items[0]
    # doc.add(item, table_name)  # add one doc
    # doc.add(items, table_name)  # add more than one docs
    #
    # # time.sleep(4) # wait commit
    # print('doc detail:', doc.detail('12113313177', table_name))  # show doc detail
    #
      # search on default field
    #
    # doc.delete('12113933131', table_name)  # delete one doc
    # # delete more than one docs
    # doc.delete(['12113933131', '12113313177'], table_name)