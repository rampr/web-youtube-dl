from django.db import models
import datetime

class Info(models.Model):
    folder = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=50,db_index=True)
    status = models.CharField(max_length=10)
    created = models.DateTimeField('date created')
    downloaded = models.DateTimeField('date completed',null=True)

    def add_to_queue(self,folder,url,title):
        self.folder = folder
        self.title = title
        self.created = datetime.datetime.now()
        self.status = "inqueue"
        self.save()
        return self.id

def update_status(id,status):
    info = Info.objects.get(pk=id)
    info.status=status

    if status == "downloaded":
        self.downloaded = datetime.datetime.now()

    info.save()
    return

def get_details(search_text):
    q  = Info.objects.filter(title__contains=str(search_text))
    return q
