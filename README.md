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


File structure:
src - 
    - Contains all the source code
    - src/calendar - contains all the google calendar api related code. 
    - Some secrets are not added since it is my(Deepak's credentials). 
    - Need to create test credentials and use.

Tasks - 
    - Contains the list of tasks for Planner. 
    - This is the project management document.

Ideas - 
    - Contains all the namespaces
    - The primary one in this is TestIdeas which contains all test tasks

