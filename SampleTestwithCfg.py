import json
import os
import sys

from libs import handler

with open('config.json') as f:
  configdata = json.load(f)

print(configdata['gcp_project_body']['projectId'])

gcp_obj = handler.Handle_GCP()

projectId = configdata['gcp_project_body']['projectId']
firebase_proj = projectId

if gcp_obj.project_exists(projectId):
    print("Project Already Exists")
else:
    print("Project Created") if gcp_obj.create_proj(configdata['gcp_project_body']) else sys.exit()

url_firebase = configdata['url_firebase']%(projectId)

if gcp_obj.get_service_key('projects/'+firebase_proj, os.path.join(os.getcwd(), 'privatekeys')):
    fireObj = handler.Handle_Firebase(serviceaccountfile=os.path.join(os.getcwd(),'key.json'))
    fireObj.add_firebase_gcp(url_firebase, configdata['firebase_project_body'])

    #Android config Download
    configure_android_url = configdata['configure_android_url']%(firebase_proj)
    fireObj.configure_android_app_to_firebase(configure_android_url, configdata['configure_android_app'])
    appId = fireObj.get_android_app_id(firebase_proj, configdata['configure_android_app']['packageName'])
    downloadandroidurl =configdata['downloadandroidurl']%(firebase_proj, appId)
    fireObj.downloadconfig(os.path.join(os.getcwd(),'op_dir'), downloadandroidurl, 'android')

    #iOS config Download
    configure_ios_url = configdata['configure_ios_url']%(firebase_proj)
    fireObj.configure_ios_app_to_firebase(configure_ios_url, configdata['configure_ios_app'])
    appId = fireObj.get_ios_app_id(firebase_proj, configdata['configure_ios_app']['bundleId'])
    downloadiosurl = configdata['downloadiosurl']%(firebase_proj, appId)
    fireObj.downloadconfig(os.path.join(os.getcwd(), 'op_dir'), downloadiosurl, 'ios')
