# Planner
Understands the task and categorizes it accordingly and schedules it in your calender. 


Script Usage:
LogIdea.py [-h] [--namespace NAMESPACE] [--idea IDEA [IDEA ...]]
                  [--todo]

This script performs the following set of actions.
* Reads the idea(logged input string)
* clusters the idea with existing ideas.
* Schedules the idea to Google Calendar
* Pushes the idea to Git hub to source control the idea

Example Usage: 
* python LogIdea.py -h
* python LogIdea.py --todo
* python LogIdea.py --namespace TestIdeas --idea <Idea without quotes>

optional arguments:
  -h, --help            show this help message and exit
  --namespace NAMESPACE
                        This is the work space for the idea. The namespace
                        contains the following: - idea.txt - time stamped idea
                        logs - log.txt - normal idea logs
  --idea IDEA [IDEA ...]
                        Idea to be logged, clustered and scheduled
  --todo                Lists tasks to do for enahancing this utility

