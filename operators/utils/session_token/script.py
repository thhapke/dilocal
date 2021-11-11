# Mock apis needs to be commented before used within SAP Data Intelligence
#from diadmin.dimockapi.mock_api import mock_api
#api = mock_api(__file__)

import os
import json
import requests
import http.client
from base64 import b64encode

LOCAL = False

def gen():

    app_id = os.environ.get("VSYSTEM_APP_ID")
    user = os.environ.get('VSYSTEM_USER')
    secret = os.environ.get("VSYSTEM_SECRET")
    tenant = os.environ.get('VSYSTEM_TENANT')

    if not user :
        user = 'teched21'
    if not tenant :
        tenant = 'default'
    if not secret :
        secret = api.config.password
    if not app_id :
        app_id = user

    r = None

    headers = {'X-Requested-With': 'XMLHttpRequest'}
    if not LOCAL :
        r = requests.get(url='http://vsystem-internal:8796/token/v2',auth=(app_id,secret),headers=headers)

    if r and r.status_code == 200 :
        api.send('logging','Requests connection')
        response = json.loads(r.text)
        data = f"{response}"
        api.send('token',data)  # data type: string
        att = {'user': user,
               'app_id': app_id,
               'tenant':tenant,
               'secret':secret}
        msg = api.Message(attributes=att,body = data)
        api.send('output',msg)  # data type: string

    # Get bearer token
    userAndPass = b64encode(bytes(app_id + ':' + secret, "utf-8")).decode("ascii")
    headers = { 'Authorization' : 'Basic %s' %  userAndPass }
    if not LOCAL :
        conn = http.client.HTTPConnection('vsystem-internal','8796')
        conn.request("GET","/token/v2", headers=headers)

        # Put auth bearer token into header
        r = conn.getresponse()

    if r and r.status == 200 :
        api.send('logging','HTTPconnection connection')
        responseText = json.loads(response.read())
        bearerHeader = { 'Authorization' : responseText['access_token'] }
        data = f"{bearerHeader}"
        att = {'user': user,
               'app_id': app_id,
               'tenant':tenant,
               'secret':secret}
        msg = api.Message(attributes=att,body = data)
        api.send('output',msg)  # data type: string
        return


    att = {'user':user,
           'tenant':tenant,
           'password':api.config.password}

    msg = api.Message(attributes=att,body = None)
    api.send('output',msg)  # data type: string

api.add_generator(gen)