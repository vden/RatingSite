from feeds.models import *
from datetime import datetime
from xml.etree.cElementTree import ElementTree as etree

def parse_feed(stream):
	tree = etree()
	tree.parse(stream)
	
	_ = lambda x: item.findtext(x)

	for item in tree.findall("channel/item"):
		blog = _("author")
		b = IndexedBlog.objects.get_or_create(url=blog)[0]
		b.save()

		dt = datetime.strptime(_("pubDate"), "%a, %d %b %Y %H:%M:%S %Z")
		article = {"pubdate": dt, "link": _("link"), "title": _("title") or "", "blog": b}
		existing = IndexedArticle.objects.filter(**article)

		if not len(existing):	
			a = IndexedArticle.objects.create(**article)		
			a.save()
			print "Add article %s..."%a.id

			for c in StatCategory.objects.all():
				f = StatAtom.objects.create(category=c, value=_("yablogs:%s"%c.name), article = a)
				f.save()
				
