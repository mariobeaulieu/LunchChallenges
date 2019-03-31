#!/usr/bin/env python
import logging
import threading
import time
import concurrent.futures

def thread_function(name):
  logging.info("Thread %s: starting",name)
  time.sleep(2)
  logging.info("Thread %s: finishing",name)

if __name__ == "__main__":
  n = 5
  format = "%(asctime)s: %(message)s"
  logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
  logging.info("Main    : before creating thread")
  x = threading.Thread(target=thread_function, args=('NoDaemon',))
  logging.info("Main    : before running thread")
  x.start()
  logging.info("Main    : wait for the thread to finish")
  x.join()
  logging.info("Main    : all done")
  # With daemon
  y = threading.Thread(target=thread_function, args=('WithDaemon',),daemon=True)
  logging.info("Main    : before running daemonized thread")
  y.start()
  logging.info("Main    : wait for the daemonized thread to finish")
  y.join()
  logging.info("Main    : all done")
  # With list
  print("\nWith a list of threads")
  threads = list()
  for i in range(n):
    logging.info("Main    : create and start thread %d.",i)
    z = threading.Thread(target=thread_function, args=(i,))
    threads.append(z)
    z.start()
  for i,thread in enumerate(threads):
    logging.info("Main    : before joining thread %d.",i)
    thread.join()
    logging.info("Main    : thread %d done.",i)
  # With concurrent futures
  print("\nWith concurrent futures")
  with concurrent.futures.ThreadPoolExecutor(max_workers=n) as ex:
    ex.map(thread_function, range(n))

