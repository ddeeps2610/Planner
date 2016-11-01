#!/usr/bin/python
from __future__ import print_function
from iCalendar import Calendar
import os
import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

class GoogleCalendar(Calendar):
  """
  This script implements the google calendar class to read and/or 
  insert entries into the google calendar.
  """
  flags = None
  SCOPES = None
  CLIENT_SECRET_FILE = None
  APPLICATION_NAME = None
  service = None

  def __init__(self):
    """
    Initializes the google calendar with various configurations.
    """
    try:
      import argparse
      self.flags = argparse.ArgumentParser(parents=[tools.argparser]).\
              parse_args()
    except ImportError:
      self.flags = None

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/calendar-python-quickstart.json
    self.SCOPES = 'https://www.googleapis.com/auth/calendar'#.readonly'
    self.CLIENT_SECRET_FILE = 'client_secret.json'
    self.APPLICATION_NAME = 'Google Calendar API Python'

    credentials = self.getCredentials()
    http = credentials.authorize(httplib2.Http())
    self.service = discovery.build('calendar', 'v3', http=http)



  def getCredentials(self):
    """
    Gets valid user credentials from storage.

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
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if self.flags:
            credentials = tools.run_flow(flow, store, self.flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


  def readEvents(self):
    """
    Reads tasks from the calendar and displays. 
    """
    print('Getting the upcoming 10 events')
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    eventsResult = self.service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


  def insertEvent(self, task=None):
    """
    This method inserts task into the calendar. The task object should
    comprise of all necessary information required by the calendar
    to insert it.
    task - task object to be inserted.
    """
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    GMT_OFF = '-07:00'
    startTime = '2016-11-1T00:00:00%s'%GMT_OFF # task.starttime
    endTime = '2016-11-1T00:00:00%s'%GMT_OFF # task.starttime + task.duration
    myEvent = {
        'summary': 'New task summary',
        'start': {'dateTime': startTime},
        'end'  : {'dateTime': endTime},
        'attendees': [
            {'email':'dma234@cornell.edu'},
        ],
    }
    print('Inserting an event')
    e = self.service.events().insert(calendarId='primary',sendNotifications=True,body=myEvent).execute()
    print('''%rEvent added:
          Start: %s
          End:   %s'''%(e['summary'].encode('utf-8'),
                        e['start']['dateTime'],e['end']['dateTime']))


if __name__ == '__main__':
  cal = GoogleCalendar()
  cal.readEvents()
  cal.insertEvent()
