import os
import sys

from libs import handler


gcp_obj = handler.Handle_GCP()

gcp_project_body = {
    "name": "gcp hwswtofme002",
    "projectId": "hwswtofme002"
}

if gcp_obj.project_exists(gcp_project_body['projectId']):
    print("Project Already Exists")
else:
    print("Project Created") if gcp_obj.create_proj(gcp_project_body) else sys.exit()

url_firebase = "https://firebase.googleapis.com/v1beta1/%s:addFirebase" % (gcp_project_body['projectId'])

fireObj = handler.Handle_Firebase()
firebase_project_body = {
    "regionCode": "IN",
    "timeZone": "Asia/Kolkata"
}
fireObj.add_firebase_gcp(url_firebase, firebase_project_body)

#
#
firebase_proj = gcp_project_body['projectId']  # "testdroid-49ee1"

configure_android_url = 'https://firebase.googleapis.com/v1beta1/projects/%s/androidApps'%(firebase_proj)
configure_android_app = {
                        "packageName": "com.example.testdroid3",
                        }

fireObj.configure_android_app_to_firebase(configure_android_url, configure_android_app)
appId = fireObj.get_android_app_id(firebase_proj, configure_android_app['packageName'])
downloadandroidurl ='https://firebase.googleapis.com/v1beta1/projects/%s/androidApps/%s/config'%(firebase_proj, appId)
fireObj.downloadconfig(os.path.join(os.getcwd(),'op_dir','android'), downloadandroidurl)

configure_ios_url = 'https://firebase.googleapis.com/v1beta1/projects/%s/iosApps' % (firebase_proj)
configure_ios_app = {
    "bundleId": "com.example.testios1",
}

fireObj.configure_ios_app_to_firebase(configure_ios_url, configure_ios_app)
appId = fireObj.get_ios_app_id(firebase_proj, configure_ios_app['bundleId'])
downloadiosurl = 'https://firebase.googleapis.com/v1beta1/projects/%s/iosApps/%s/config' % (firebase_proj, appId)
fireObj.downloadconfig(os.path.join(os.getcwd(), 'op_dir', 'ios'), downloadiosurl)
