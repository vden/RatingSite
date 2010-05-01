from django.core.management.base import NoArgsCommand
import settings
from feeds.views import parse_feed
from urllib2 import urlopen

class Command(NoArgsCommand):
	help = "Process defined feeds."
	
	def handle_noargs(self, **options):
		for feed in settings.YA_FEEDS:
			print u"Loading feed %s"%feed

			f = urlopen(feed)
			parse_feed(f)
