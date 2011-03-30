import sys
import time

from gearman import GearmanClient, Task

client = GearmanClient(["127.0.0.1"])

i = 0
while 1:
   client.dispatch_background_task('speak', i)
   print 'Dispatched %d' % i
   i += 1
   time.sleep(1)
