import time

from gearman import GearmanWorker

def speak(job):
  print job.arg 

worker = GearmanWorker("[127.0.0.1]")
worker.register_function("speak", speak)
worker.work()
