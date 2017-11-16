#!/usr/bin/python

"""
This script logs the idea in Ideas.txt file with time stamp.
"""
import datetime
import os,sys
import argparse
import textwrap


ideasPath = '../Ideas/'
ideaFileName = 'ideas.txt'
logFileName = 'log.txt'


def readArgs():
    """
    This function sets up argument parsing and returns a list of arguments.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        This script performs the following set of actions.
        * Reads the idea(logged input string)
        * clusters the idea with existing ideas.
        * Schedules the idea to Google Calendar
        * Pushes the idea to Git hub to source control the idea

        Example Usage: 
        * python LogIdea.py -h
        * python LogIdea.py --todo
        * python LogIdea.py --namespace TestIdeas --idea <Idea without quotes>
	'''))
    parser.add_argument('--namespace', 
	help=textwrap.dedent('''\
        This is the work space for the idea. The namespace contains the 
        following:
        - idea.txt - time stamped idea logs
        - log.txt  - normal idea logs
	'''))
    parser.add_argument('--idea',
        nargs='+',
        help="Idea to be logged, clustered and scheduled")
    parser.add_argument('--todo', 
        action='store_true',
        help="Lists tasks to do for enahancing this utility")
    args = parser.parse_args()
    return args


def todo():
    """
    Lists tasks to do.
    """
    print "* Store the clustering result and build on top of it instead of clustering all over again."
    print "* Push the idea to the source control."
    print "* Add Kubernetes container to make it work on all platforms"
    print "* Print option to print all clusters from existing inputs"


def saveIdeaToFiles(ideaFilePath, logFilePath, idea):
    """
    Saves the idea to idea.txt and log.txt.
    ideaFilePath - Path to the idea.txt file
    logFilePath - Path to the log.txt file
    idea - idea to be logged.
    """
    ideaFile = None
    logFile = None

    if os.path.exists(ideaFilePath):
        ideaFile = open(ideaFilePath, 'a+')
    else: 
        ideaFile = open(ideaFilePath, 'w+')
  
    if os.path.exists(logFilePath):
        logFile = open(logFilePath, 'a+')
    else:
        logFile = open(logFilePath, 'w+')
    
   
    # Save the idea in the ideas.txt and log.txt 
    idea = ''.join([word+' ' for word in args.idea]) + '\n'
    log = str(datetime.datetime.now()) + " " + idea
    ideaFile.write(idea)
    logFile.write(log)
    ideaFile.close()
    logFile.close()

   

def clusterizeIdea(ideaFilePath, idea): 
    """
    Clusters the idea with existing ideas.
    ideaFilePath - File path of idea.txt which contains the existing ideas for
        the given namespace.
    idea - The idea to be clustered.
    """
    from sentenceClusterer import Clusterer
    clusterer = Clusterer(train=True, ideasFile=ideaFilePath)
    clusterer.clusterSentence(idea)


def getNameSpacePath(namespace):
    """
    Generate path for the namespace. If the path doesn't exist, create one.
    namespace - Namespace for the idea grouping.
    """
    path = os.path.join(ideasPath, namespace)
    if os.path.exists(path):
        print 'Path {} exists'.format(path)
    else:
        print 'Path {} does not exist'.format(path)
        print 'Creating the namespace {}'.format(path)
        os.makedirs(path)
    return path 


def Main(args):
    """
    Main method that processes the input arguments.
    args - Arguments passed to the script.
    """
    if args.todo:
        todo()
        sys.exit() 
   
    # Get path for the name space 
    path = getNameSpacePath(args.namespace)

    # Convert idea list to string.
    idea = ''.join([word+' ' for word in args.idea]) + '\n'


    # Process namespace
    # Step1: Save idea to the idea.txt and log.txt files.
    ideaFilePath = os.path.join(path, ideaFileName)
    logFilePath = os.path.join(path, logFileName)
    saveIdeaToFiles(ideaFilePath, logFilePath, idea)

  
    # Process ideas for
    # Step 2: Clustere idea with existing ideas
    if os.path.exists(ideaFilePath):
        clusterizeIdea(ideaFilePath, idea)
    else:
        print "Idea File Path : {} does not exist".format(ideaFilePath)

    # Step 3: Schedule idea on the google calendar





###############################################################################
#                                    MAIN                                     #
###############################################################################
if __name__ == "__main__":
    args = readArgs()
    print args
    Main(args) 
