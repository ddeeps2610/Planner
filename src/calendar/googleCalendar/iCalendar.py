#!/usr/bin/python
"""
This script defines the interface for the calendar updates.
"""

class Calendar():
  """
  Verifies the credentials and adds tasks to calendar.
  """
  def getCredentials(self):
    """
    Fetches the credentials for the calendar. This is specific to the
    calendar. Thus needs to be overriden by the specific calendar 
    implementation.
    """
    raise NotImplementedError

  def readEvents(self):
    """
    Reads tasks from the calendar and displays. This is specific 
    implementation for the calendar implementations and needs to be
    overridden.
    """
    raise NotImplementedError

  def insertEvent(self, task):
    """
    This method inserts task into the calendar. The task object should
    comprise of all necessary information required by the calendar
    to insert it.
    task - task object to be inserted.
    """
    raise NotImplementedError
    
