from django.shortcuts import render_to_response
from django.template import RequestContext

from feeds.models import StatAtom

def index(request):
#	cats = ['links', 'comments', 'commenters']
	cats = [ 'commenters', 'links']
	atoms = []	

	main_atoms =  StatAtom.objects.order_by('-value').filter(category__name = 'comments')[:20]

	atoms.append(main_atoms)
	for c in cats: 
		r = []
		for b in [x.blog for x in atoms[0]]:
			r.append ( StatAtom.objects.get(blog=b, category__name=c) )

		atoms.append( r )

	atoms = zip(*atoms)

	my = []
	in_top = True

	if request.session.has_key("openid_name"):
		in_top = request.session["openid_name"] in [ x.blog.url for x in main_atoms ]

		if not in_top:
			st = StatAtom.objects.order_by('-value').filter(category__name = 'comments',blog__url = request.session["openid_name"])

			if not len(st): my = None
			else:
				my.append( st[0] )

				for c in cats:
					st = StatAtom.objects.filter(blog__url = request.session["openid_name"], category__name=c)
					my.extend ( [ st[0], ] )

	return render_to_response("rating/index.html", {'atoms': atoms, 'in_top': in_top, 'my': my}, context_instance=RequestContext(request))
