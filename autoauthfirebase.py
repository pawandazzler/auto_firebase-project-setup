import os

def set_project(self, project_id):
    stream = os.popen(
        'gcloud config set project %s'%(project_id))
    output = stream.read()
    if 'Updated property [core/project]' in output:
        return True
    return False
