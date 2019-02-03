#!/usr/bin/python

# Task Planner
# Given a number of tasks all requiring 1 unit of time
# and each having a deadline and a reward, maximize
# the task planning

import random

class Task:
    # reward and deadline are integers
    def __init__(self, reward, deadline):
        self.reward   = reward
        self.deadline = deadline

    def getReward(self):
        return self.reward

    def getDeadline(self):
        return self.deadline

    def printTask(self):
        print '[$%i,%idays]'%(self.getReward(),self.getDeadline()),

class Schedule:
    def __init__(self, numTasks, maxDeadline):
        # Initial schedule is free (=iNone) for all timeslots
        self.schedule    = [None for i in range(maxDeadline)]
        self.listOfTasks = []
        self.numTasks    = numTasks
        # Generate the tasks
        for i in range(numTasks):
            #self.listOfTasks.append(Task(random.randint(1,9),random.randint(0,maxDeadline-1)))
            self.listOfTasks.append(Task(i,random.randint(0,maxDeadline-1)))

    def printTasks(self):
        print "This is the list of tasks:"
        for i in self.listOfTasks:
            i.printTask()
        print

    def sortTasksByReward(self):
        # Push the lowest rewards at the end of the list
        for i in range(self.numTasks-1):
            for j in range(self.numTasks-i-1):
                if self.listOfTasks[j].getReward() < self.listOfTasks[j+1].getReward():
                   self.listOfTasks[j],self.listOfTasks[j+1] = self.listOfTasks[j+1],self.listOfTasks[j]

    def addTaskToSchedule(self, t):
        # This routine add tasks as late as possible in the schedule
        for i in range(t.getDeadline(),-1,-1):
            if self.schedule[i] is None:
               # We just found an empty spot in the schedule.
               # We could put the task here, but the current task has less value than the previous
               # tasks so we should put the current task at the deadlne and move everything else
               # 1 day earlier
               for j in range(i,t.getDeadline()):
                   self.schedule[j] = self.schedule[j+1]
               self.schedule[t.getDeadline()]=t
               break

    def run(self):
        v=0
        print 'Initially...'
        self.printTasks()
        print 'Sorting tasks with highest rewards first'
        self.sortTasksByReward()
        self.printTasks()
        print 'Schedule:'
        for t in self.listOfTasks:
            self.addTaskToSchedule(t)
        for t in self.schedule:
            if t is None:
               print '[$0,0days]',
            else:
               t.printTask()
               v += t.getReward()
        print
        print 'Total value: $%i'%(v)


d = input('How many days to schedule: ')
n = input('Enter number of tasks to schedule: ')
s = Schedule(n,d)
s.run()

