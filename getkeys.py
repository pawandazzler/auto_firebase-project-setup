from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()

service = discovery.build('iam', 'v1', credentials=credentials)

project = 'projects/testdroid-49ee1'
request = service.projects().serviceAccounts().list(name=project)

service_account = ''
while True:
    response = request.execute()

    for service_account in response.get('accounts', []):
        service_account = service_account['email']

    request = service.projects().serviceAccounts().list_next(previous_request=request, previous_response=response)
    if request is None:
        break

pprint(service_account)

name1='%s/serviceAccounts/%s'%(project,service_account)
#name2='projects/second-replica-308709/serviceAccounts/firebase-adminsdk-zt7o8@second-replica-308709.iam.gserviceaccount.com'
# TODO: Update placeholder value.

create_service_account_key_request_body = {
    # TODO: Add desired entries to the request body.
}

all_roles = \
    {
"bindings": [
                {
                  "role": "roles/resourcemanager.projectIamAdmin",
                  "members": [
                    "serviceAccount:firebase-adminsdk-6k26c@testdroid-49ee1.iam.gserviceaccount.com"
                  ]
                }
              ]
    }

print(service.projects().serviceAccounts().getIamPolicy(resource=name1).execute())
#print(service.projects().serviceAccounts().setIamPolicy(resource=name1).execute())
#print(service.projects().serviceAccounts().getIamPolicy(resource=name1).execute())
#print(dir(service.projects().serviceAccounts().setIamPolicy(resource=name1)))

request = service.projects().serviceAccounts().get(name=name1)
#request = service.projects().serviceAccounts().keys().create(name=name1, body=create_service_account_key_request_body)
response = request.execute()

pprint(response)