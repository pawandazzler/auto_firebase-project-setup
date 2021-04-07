# auto_firebase-project-setup
Mandatory to have python 3.7 + version

pip install -r requirements.txt

config.json is configuration file

Note :-
Project is still in development phase, current this throws exception with Enable API for service account.
Tested on windows only

---------------------------------Console logs---------------------------------------------------------
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

(venv) C:\Users\Pawan\PycharmProjects\auto_firebase project setup>python SampleTestwithCfg.py
firm-aviary-308417
##################################################
Handle_GCP InIt
project_exists Init
Project Already Exists
get_service_key Init :  projects/firm-aviary-308417
{'accounts': [{'name': 'projects/firm-aviary-308417/serviceAccounts/firm-aviary-308417@firm-aviary-308417.iam.gserviceaccount.com', 'projectId': 'firm-aviary-308417'
, 'uniqueId': '108198411729407295371', 'email': 'firm-aviary-308417@firm-aviary-308417.iam.gserviceaccount.com', 'displayName': 'firm-aviary-308417', 'etag': 'MDEwMj
E5MjA=', 'oauth2ClientId': '108198411729407295371'}]}
service_account :  firm-aviary-308417@firm-aviary-308417.iam.gserviceaccount.com
Updated property [core/project].

set_project :  True
getkey_cmd :  gcloud iam service-accounts keys create key.json --iam-account=firm-aviary-308417@firm-aviary-308417.iam.gserviceaccount.com
created key [72683df20698a36f46216e74b1e9d0069fcabe3b] of type [json] as [key.json] for [firm-aviary-308417@firm-aviary-308417.iam.gserviceaccount.com]

##################################################
Handle_Firebase InIt
add_FireBase_GCP Init
<h1>Not Found</h1>
<h2>Error 404</h2>

configure_android_app_to_firebase InIt
URL to Configure Android App :  https://firebase.googleapis.com/v1beta1/projects/firm-aviary-308417/androidApps
{
  "error": {
    "code": 403,
    "message": "Firebase Management API has not been used in project 218529736936 before or it is disabled. Enable it by visiting https://console.developers.google.c
om/apis/api/firebase.googleapis.com/overview?project=218529736936 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our
 systems and retry.",
    "status": "PERMISSION_DENIED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.Help",
        "links": [
          {
            "description": "Google developers console API activation",
            "url": "https://console.developers.google.com/apis/api/firebase.googleapis.com/overview?project=218529736936"
          }
        ]
      },
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "SERVICE_DISABLED",
        "domain": "googleapis.com",
        "metadata": {
          "service": "firebase.googleapis.com",
          "consumer": "projects/218529736936"
        }
      }
    ]
  }
}

get_android_app_id Init
{'error': {'code': 403, 'message': 'Firebase Management API has not been used in project 218529736936 before or it is disabled. Enable it by visiting https://console
.developers.google.com/apis/api/firebase.googleapis.com/overview?project=218529736936 then retry. If you enabled this API recently, wait a few minutes for the action
 to propagate to our systems and retry.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Goog
le developers console API activation', 'url': 'https://console.developers.google.com/apis/api/firebase.googleapis.com/overview?project=218529736936'}]}, {'@type': 't
ype.googleapis.com/google.rpc.ErrorInfo', 'reason': 'SERVICE_DISABLED', 'domain': 'googleapis.com', 'metadata': {'service': 'firebase.googleapis.com', 'consumer': 'p
rojects/218529736936'}}]}}
Traceback (most recent call last):
  File "SampleTestwithCfg.py", line 31, in <module>
    appId = fireObj.get_android_app_id(firebase_proj, configdata['configure_android_app']['packageName'])
  File "C:\Users\Pawan\PycharmProjects\auto_firebase project setup\libs\handler.py", line 149, in get_android_app_id
    for i, app in enumerate(d for d in apps_json['apps']):
KeyError: 'apps'

