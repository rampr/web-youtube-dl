from django.shortcuts import render_to_response
from django.http import HttpResponse
from downloader.download.models import *
from gearman import GearmanClient,Task
from django.conf import settings

def index(request):
    return render_to_response('download/index.html', {})

def download(request):

    if "folder" not in request.GET or "title" not in request.GET or "url" not in request.GET:
        return HttpResponse("failed to enqueue, one or more params missing")
    
    folder = request.GET["folder"]
    name = request.GET["title"]
    video_url = request.GET["url"]

    if folder =='' or name =='' or video_url=='':
        return HttpResponse("failed to enqueue")
    
    info = Info()
    video_id = info.add_to_queue(folder,video_url,name)

    #outtmpl="%s/%s" % (folder,name)

    folder="%s/%s" %(settings.DOWNLOAD_PATH,folder)

    d = {'folder':folder,'name':name,'url':video_url,'id':video_id}

    client = GearmanClient(["127.0.0.1"])
    res = client.dispatch_background_task("download", d)
    return HttpResponse("enqueued video for successfully")

def search(request):

    if "search_text" in request.GET:
        search_text = request.GET["search_text"]
    else:
        return HttpResponse("error, params needed")
    
    if search_text == '':
        return HttpResponse("no query string given")
    
    info = get_details(search_text)
    return render_to_response('download/search.html', {'info':info})
        
