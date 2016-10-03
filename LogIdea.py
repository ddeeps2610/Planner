#/usr/bin/python

"""
This script logs the idea in Ideas.txt file with time stamp.
"""
import datetime
import os,sys

message = ''.join([word+' ' for word in sys.argv[1:]]) + '\n'
message = str(datetime.datetime.now()) + " " + message

fp = None
filePath = 'Ideas.txt'
if os.path.exists(filePath):
  with open(filePath, 'ab+') as fp:
    fp.write(message)
else:
  with open(filePath, 'wb+') as fp:
    fp.write(message)

