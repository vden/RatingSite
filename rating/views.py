from django.shortcuts import render_to_response
from django.template import RequestContext

from feeds.models import StatAtom

def index(request):
#	cats = ['links', 'comments', 'commenters']
	cats = [ 'commenters', 'links']
	atoms = []	

	atoms.append( StatAtom.objects.order_by('-value').filter(category__name = 'comments')[:20] )
	for c in cats: 
		r = []
		for b in [x.blog for x in atoms[0]]:
			r.append ( StatAtom.objects.get(blog=b, category__name=c) )

		atoms.append( r )

	atoms = zip(*atoms)       	

	return render_to_response("rating/index.html", {'atoms': atoms}, context_instance=RequestContext(request))
