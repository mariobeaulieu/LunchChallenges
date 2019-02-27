#!/usr/bin/python

from subprocess import Popen
from threading import Timer

pid=0

def killit():
   Popen('kill -9 '+str(pid),shell=True)
   print 'Killed process ',pid

def run(cmd, timeout):
   global pid
   print 'proc = Popen(',cmd,',shell=True)'
   proc = Popen(cmd,shell=True)
   timer = Timer(timeout, killit)
   pid = proc.pid
   print 'Process ID is ',pid
   timer.start()
   print 'stdout,stderr = proc.communicate()'
   stdout,stderr = proc.communicate()
   timer.cancel()
   print 'proc.returncode=',
   print proc.returncode

timeout = 1
while timeout>0:
   timeout = input('Enter timeout:')
   if timeout>0:
      cmd = input('Enter command between quotes: ')
      run(cmd,timeout)

