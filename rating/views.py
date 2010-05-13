from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from feeds.models import StatAtom, IndexedBlog, IndexedArticle, BlogInfoForm
from rating.models import TakeRequest
from django.db.models import Sum

def index(request):
#	cats = ['links', 'comments', 'commenters']
	cats = [ 'commenters', 'links']
	atoms = []

	main_atoms =  StatAtom.objects.filter(category__name = 'comments').values("article__blog__url", "article__blog", "article__blog__owner_name").annotate(value=Sum("value")).order_by('-value')[:20]
#	main_atoms = [ x["dval"] for x in main_atoms  ]

	atoms.append(main_atoms)
	for c in cats: 
		r = []
		for b in [x["article__blog"] for x in atoms[0]]:
			sss = StatAtom.objects.filter(article__blog=b, category__name=c).values("article__blog").annotate(value=Sum("value"))[0]
			r.append(sss)
		atoms.append( r )

	atoms = zip(*atoms)

	print atoms

	my = []
	in_top = True

	if request.session.has_key("openid_name"):
		in_top = request.session["openid_name"] in [ x["article__blog__url"] for x in main_atoms ]

		if not in_top:
			st = StatAtom.objects.filter(category__name = 'comments',article__blog__url = request.session["openid_name"]).values("article__blog", "article__blog__url", "article__blog__owner_name").annotate(value=Sum("value"))

			if not len(st): my = None
			else:
				my.append( st[0] )

				for c in cats:
					st = StatAtom.objects.filter(article__blog__url = request.session["openid_name"], category__name=c).values("article__blog").annotate(value=Sum("value")) 
					my.extend ( [ st[0], ] )
					
	return render_to_response("rating/index.html", {'atoms': atoms, 'in_top': in_top, 'my': my}, context_instance=RequestContext(request))

def card(request, blog_id):
	blog = get_object_or_404(IndexedBlog, id=blog_id)
	message = request.GET.get("message", None)

	my = []
	cats = [ 'commenters', 'links' ]

	st = StatAtom.objects.filter(category__name = 'comments', article__blog = blog).values("article__blog", "article__blog__url", "article__blog__owner__id", "article__blog__description", "article__blog__owner_name").annotate(value=Sum("value"))

	if not len(st): my = None
	else:
		my.append( st[0] )
		for c in cats:
			st = StatAtom.objects.filter(article__blog = blog, category__name=c).values("article__blog").annotate(value=Sum("value")) 
			my.extend ( [ st[0], ] )

	form = BlogInfoForm(instance=blog)

	return render_to_response("rating/card.html", {'my': my, 'message': message, "form": form}, context_instance=RequestContext(request))

def save_info(request, blog_id):
	blog = get_object_or_404(IndexedBlog, id=blog_id)
	frm = BlogInfoForm(request.POST, instance=blog)
	
	try:
		frm.save()
	except:
		print "ERR" 	
	print frm.cleaned_data
		
	message = u"Description updated."
	
	return HttpResponseRedirect("/rating/card/%s/?message=%s"%(blog_id, message))

def take(request, blog_id):
	blog = get_object_or_404(IndexedBlog, id=blog_id)
	
	if request.session.has_key("openid_name"):
		if request.session["openid_name"] == blog.url:
			blog.owner = request.user
			blog.save()
			message = u"This page is yours now."
		else:
			tr = TakeRequest.objects.create(author = request.user, blog = blog, description = request.POST.get("message", u""))
			tr.save()
			message = u"Your request sent to moderator. You'll be notified for moderator's review on your request."

	else:
		message = u"First log in, please."

	return HttpResponseRedirect("/rating/card/%s/?message=%s"%(blog_id, message))

def approve_request(request, rid):
	req = get_object_or_404(TakeRequest, id=rid)
	
	req.blog.owner = req.author
	req.blog.save()
	req.delete()

	return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

def reject_request(request, rid):
	req = get_object_or_404(TakeRequest, id=rid)
	
	req.delete()

	return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))	

def articles(request, blog_id, category_id):
	blog = get_object_or_404(IndexedBlog, id=blog_id)

	articles = IndexedArticle.objects.filter(blog = blog).order_by('-pubdate')
	r = []

	blog = get_object_or_404(IndexedBlog, id=blog_id)
	my = []
	cats = [ 'commenters', 'links' ]

	st = StatAtom.objects.filter(category__name = 'comments', article__blog = blog).values("article__blog", "article__blog__url", "article__blog__owner__id", "article__blog__owner_name").annotate(value=Sum("value"))

	if not len(st): my = None
	else:
		my.append( st[0] )
		for c in cats:
			st = StatAtom.objects.filter(article__blog = blog, category__name=c).values("article__blog").annotate(value=Sum("value")) 
			my.extend ( [ st[0], ] )

	for a in articles:
		r.append( {'article': a, 'stats': StatAtom.objects.get(article = a, category__name = category_id)} )

	return render_to_response("rating/articles.html", {'my': my, 'info': r, "category_id": category_id}, context_instance=RequestContext(request))

def archive(request):
	return render_to_response(u"rating/index.html", {})
