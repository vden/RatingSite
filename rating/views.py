from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from feeds.models import StatAtom, IndexedBlog, IndexedArticle
from rating.models import TakeRequest


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

def card(request, blog_id):
	blog = get_object_or_404(IndexedBlog, id=blog_id)
	message = request.GET.get("message", None)

	my = []
	cats = [ 'commenters', 'links']

	st = StatAtom.objects.order_by('-value').filter(category__name = 'comments', blog = blog)

	if not len(st): my = None
	else:
		my.append( st[0] )
		for c in cats:
			st = StatAtom.objects.filter(blog = blog, category__name=c)
			my.extend ( [ st[0], ] )

	return render_to_response("rating/card.html", {'my': my, 'message': message}, context_instance=RequestContext(request))

def take(request, blog_id):
	blog = get_object_or_404(IndexedBlog, id=blog_id)
	
	if request.session.has_key("openid_name"):
		if request.session["openid_name"] == blog.url:
			blog.owner = request.user
			blog.save()
			message = u"This page is yours now."
		else:
			tr = TakeRequest.objects.create(author = request.user, blog = blog, description = u"")
			tr.save()
			message = u"Your request sent to moderator. You'll be notified for moderator's review on your request."

	else:
		message = u"First log in, please."

	return HttpResponseRedirect("/rating/card/%s/?message=%s"%(blog_id, message))
