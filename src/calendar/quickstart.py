from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/tasks-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/tasks.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Tasks API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'tasks-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Tasks API.

    Creates a Google Tasks API service object and outputs the first 10
    task lists.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('tasks', 'v1', http=http)

    taskBody = {
      #"status": "needsAction",
      "kind": "tasks#task",
      "updated": datetime.datetime.now().isoformat(' '),
      #"parent": "A String", 
      #"links": None,
      "title": "Planner task", # Title of the task.
      #"deleted": False,
      "#due": datetime.datetime(2017,2,23,1,2,3,123456).isoformat(' '),
      "etag": "eTag", 
      #"notes": "Notes describing the task. Optional :P",
      #"position": "0", 
      #"hidden": False, 
      "id": "planer", 
      "selfLink": "http://www.deepakawari.com/planner", 
      }

    #service.tasklists().insert(body=taskBody).execute()
    results = service.tasklists().list(maxResults=10).execute()
    items = results.get('items', [])
    if not items:
        print('No task lists found.')
    else:
        print('Task lists:')
        for item in items:
            print('{0} ({1})'.format(item['title'], item['id']))

if __name__ == '__main__':
    main()

