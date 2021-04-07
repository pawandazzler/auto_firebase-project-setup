import json
import os
import sys

import google
import googleapiclient
from google.auth.transport import requests
from google.auth.transport.requests import AuthorizedSession
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def direct_conn():
    _scopes = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/firebase"
    ]

    credentials, project_id = google.auth.default(scopes=_scopes)
    credentials.refresh(requests.Request())
    return credentials  # credentials.token


class Handle_GCP:
    def __init__(self):
        print('#' * 50)
        print('Handle_GCP InIt')
        self._credentials = GoogleCredentials.get_application_default()

        self._service_cloudresourcemanager = discovery.build('cloudresourcemanager', 'v1', credentials=self._credentials)
        self._projects_cloudresourcemanager = self._service_cloudresourcemanager.projects()

        self._service_iam = discovery.build('iam', 'v1', credentials=self._credentials)
        self._projects_iam = self._service_iam.projects()

    def create_proj(self, proj_body):
        print("create_Proj Init")
        try:
            req = self._projects.create(body=proj_body)
            res = req.execute()
            return self.project_exists(proj_body['projectId'])
        except googleapiclient.errors.HttpError as ex:
            print(str(ex))

    def project_exists(self, project_id):
        print("project_exists Init")
        req = self._projects_cloudresourcemanager.get(projectId=project_id)

        res = req.execute()
        if res['lifecycleState'] == 'ACTIVE':
            return True
        return False

    def set_project(self, project_id):
        try:
            cmd = 'gcloud config set project %s' % (project_id)
            print(os.popen(cmd).read())
            return True
        except Exception as ex:
            print(str(ex))
            sys.exit()

    def create_service_account(self, project_id, name, display_name):

        my_service_account = self._projects_iam.serviceAccounts().create(
            name='projects/' + project_id,
            body={
                'accountId': name,
                'serviceAccount': {
                    'displayName': display_name
                }
            }).execute()

        print('Created service account: ' + my_service_account['email'])
        return my_service_account['email']

    def get_service_account_email(self, project):
        request = self._projects_iam.serviceAccounts().list(name=project)
        service_account = ''
        while True:
            response = request.execute()
            print(response)
            for service_account in response.get('accounts', []):
                service_account = service_account['email']
            request = self._service_iam.projects().serviceAccounts().list_next(previous_request=request,
                                                                     previous_response=response)
            if request is None:
                break

        print("service_account : ", service_account)
        if len(service_account) <= 0:
            print("Service Account was not found for project " + project)
            prj = project.split('/')[1]
            return self.create_service_account(project_id=prj, name=prj, display_name=prj)
        else:
            return service_account

    def get_service_key(self, project, path):
        print("get_service_key Init : ", project)

        service_account = self.get_service_account_email(project)

        isset = self.set_project(project.split('/')[1])
        print("set_project : ", isset)
        if isset:
            getkey_cmd = 'gcloud iam service-accounts keys create key.json --iam-account=%s' % (service_account)
            print("getkey_cmd : ", getkey_cmd)
            try:
                stream = os.popen(getkey_cmd)
                output = stream.read()
                print(output)
                import time
                time.sleep(5)
                return True
            except Exception as ex:
                return False

class Handle_Firebase:
    def __init__(self, serviceaccountfile):
        print('#' * 50)
        print('Handle_Firebase InIt')
        self._scopes = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/firebase"
        ]
        self._credentials = service_account.Credentials.from_service_account_file(
            os.path.join(serviceaccountfile), scopes=self._scopes)  # 'testdroid.json'
        self._request = Request()
        self._credentials.refresh(self._request)
        self._access_token = self._credentials.token
        self._authed_session = AuthorizedSession(direct_conn())  # self._credentials

    def add_firebase_gcp(self, url, request_body):
        print("add_FireBase_GCP Init")
        request_body = request_body
        headers = {"Content-Type": "application/json"}
        res = self._authed_session.post(url, headers=headers, json=request_body)
        print(res.text)

    def get_android_app_id(self, project, packagename):
        print("get_android_app_id Init")
        url = "https://firebase.googleapis.com/v1beta1/projects/%s/androidApps" % (project)
        apps_json = json.loads(self._authed_session.get(url).content)
        print(apps_json)
        for i, app in enumerate(d for d in apps_json['apps']):
            print(i, app['packageName'])
            if app['packageName'] == packagename:
                print(app['appId'])
                return app['appId']

    def get_ios_app_id(self, project, packagename):
        print("get_ios_app_id Init")
        url = "https://firebase.googleapis.com/v1beta1/projects/%s/iosApps" % (project)
        apps_json = json.loads(self._authed_session.get(url).content)
        print(apps_json)
        for i, app in enumerate(d for d in apps_json['apps']):
            print(i, app['bundleId'])
            if app['bundleId'] == packagename:
                print(app['appId'])
                return app['appId']

    def configure_android_app_to_firebase(self, url, request_body):
        print("configure_android_app_to_firebase InIt")
        print("URL to Configure Android App : ", url)
        request_body = request_body
        headers = {"Content-Type": "application/json"}
        res = self._authed_session.post(url, headers=headers, json=request_body)
        print(res.text)

    def configure_ios_app_to_firebase(self, url, request_body):
        print("configure_ios_app_to_firebase InIt")
        print("URL to Configure iOS App : ", url)
        request_body = request_body
        headers = {"Content-Type": "application/json"}
        res = self._authed_session.post(url, headers=headers, json=request_body)
        print(res.text)

    def downloadconfig(self, path, url, opfile):
        print("downloadconfig  InIt")
        if os.path.isdir(path):
            print("Path to Download : ", path)
            print("URL to get from : ", url)
            content = json.loads(self._authed_session.get(url).content)
            print("content : ", content)
            with open(os.path.join(path, opfile + '.json'), 'w') as op:
                json.dump(content, op, ensure_ascii=True, indent=4, sort_keys=True)
        else:
            print("Path is either not a directory or doesn't exist at all")
