from feeds.models import *

from datetime import datetime
from xml.etree.cElementTree import ElementTree as etree

def parse_feed(stream):
	tree = etree()
	tree.parse(stream)
	
	_ = lambda x: item.findtext(x)

	stats = StatCategory.objects.all()

	counter = 1
	lst = tree.findall("channel/item")
	for item in lst:
		blog = _("author")
		b = IndexedBlog.objects.get_or_create(url=blog)[0]
		b.save()

		dt = datetime.strptime(_("pubDate"), "%a, %d %b %Y %H:%M:%S %Z")
		article = {"pubdate": dt, "link": _("link"), "title": _("title") or "", "blog": b}

		print "Loading %s of %s..."%(counter, len(lst))
		for c in stats:
			val =  _("{urn:yandex-blogs}%s"%c.name) or 0
			try:
				sa = StatAtom.objects.get(blog=b, category=c)
				sa.update_value(val, dt )
                        except StatAtom.DoesNotExist:
				sa = StatAtom.objects.create(blog=b, category=c, value=val, updated=dt)
				sa.save()

		counter += 1
#		existing = IndexedArticle.objects.filter(**article)
#		if not len(existing):	
#			a = IndexedArticle.objects.create(**article)		
#			a.save()
#			print "Add article %s..."%a.id

#			for c in StatCategory.objects.all():
#				f = StatAtom.objects.create(category=c, value=_("yablogs:%s"%c.name) or -1, article = a)
#				f.save()

