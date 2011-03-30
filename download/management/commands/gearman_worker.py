from django.core.management.base import BaseCommand, CommandError
from downloader.download.models import *

import time
from gearman import GearmanWorker
from youtube import *

def download(job):
  print "Job received"
  d = eval(job.arg)
  outtmpl = "%s/%s" % (d["folder"],d["name"])
  video_url =  d["url"]
  video_id = d["id"]
  print outtmpl
  print video_url
  print video_id

  update_status(video_id,"downloading")

  # Information extractors
  youtube_ie = YoutubeIE()
  metacafe_ie = MetacafeIE(youtube_ie)
  dailymotion_ie = DailymotionIE()
  youtube_pl_ie = YoutubePlaylistIE(youtube_ie)
  youtube_user_ie = YoutubeUserIE(youtube_ie)
  youtube_search_ie = YoutubeSearchIE(youtube_ie)
  google_ie = GoogleIE()
  google_search_ie = GoogleSearchIE(google_ie)
  photobucket_ie = PhotobucketIE()
  yahoo_ie = YahooIE()
  yahoo_search_ie = YahooSearchIE(yahoo_ie)
  generic_ie = GenericIE()

  # File downloader
  fd = FileDownloader({
    'usenetrc': None,
    'username': None,
    'password': None,
    'quiet': False,
    'forceurl': None,
    'forcetitle': None,
    'forcethumbnail': None,
    'forcedescription': None,
    'simulate': False,
    'format': None,
    'format_limit': None,
    'outtmpl': outtmpl,
    'ignoreerrors': False,
    'ratelimit': None,
    'nooverwrites': False,
    'retries': 10,
    'continuedl': True,
    'noprogress': False,
    'playliststart': 1,
    })
  fd.add_info_extractor(youtube_search_ie)
  fd.add_info_extractor(youtube_pl_ie)
  fd.add_info_extractor(youtube_user_ie)
  fd.add_info_extractor(metacafe_ie)
  fd.add_info_extractor(dailymotion_ie)
  fd.add_info_extractor(youtube_ie)
  fd.add_info_extractor(google_ie)
  fd.add_info_extractor(google_search_ie)
  fd.add_info_extractor(photobucket_ie)
  fd.add_info_extractor(yahoo_ie)
  fd.add_info_extractor(yahoo_search_ie)

  # This must come last since it's the
  # fallback if none of the others work
  fd.add_info_extractor(generic_ie)

  # Maybe do nothing
  url = [video_url]
  print url
  retcode = fd.download(url)
  print retcode
  print type(retcode)
  print "Sleeing for 1 second"
  time.sleep(1)
  if retcode == 0:
    update_status(video_id,"downloaded")
  else:
    update_status(video_id,"error")

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
      print "worker started"
      worker = GearmanWorker(["127.0.0.1"])
      worker.register_function("download", download)
      worker.work()
