from gearman import GearmanClient,Task

client = GearmanClient(["127.0.0.1"])
#res = client.do_task(Task("echo", "foo"))
res = client.dispatch_background_task("echo", "foo")
print res
