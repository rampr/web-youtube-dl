from gearman import GearmanWorker

def echo(job):
  print job.arg
  return job.arg

worker = GearmanWorker(["127.0.0.1"])
#worker.register_function("echo", lambda job:job.arg)
worker.register_function("echo", echo)
worker.work()
