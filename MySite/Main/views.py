# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from comments.models import Comment
from .models import Post
from .forms import PostForm
from comments.forms import CommentForm


def post_create(request):
	#if not request.user.is_staff or not request.user.is_superuser:
	#	raise Http404

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "저장되었습니다.")
		return HttpResponseRedirect(instance.get_absolute_url())
	#if request.method == "POST":
	#	print "title"+request.POST.get("content")
	#	title = request.POST.get("title")
	#	Post.objects.create(title=title)
	context = {
		"form":form,
	}
	return render(request, "html/post_form.html", context)

def post_detail(request, id=None):
	#instance = Post.objects.get(id=1)
	instance = get_object_or_404(Post, id=id)
	initial_data = {
			"content_type":instance.get_content_type,
			"object_id":instance.id
	}
	
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid():
		c_type = form.cleaned_data.get("content_type")
		content_type =ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
		new_comment, create = Comment.objects.get_or_create(
									user = request.user,
									content_type = content_type,
									object_id = obj_id,
									content = content_data
								)
		if create:
			print("Yeah it Worked")
		
	comments = instance.comments	
	context = {
		"title": instance.title,
		"Login": "Login",
		"instance": instance,
		"comments": comments,
		"comment_form": form,
	}
	return render(request, "html/post_detail.html", context)

def post_list(request):
	queryset_list = Post.objects.all()#.order_by("-timestamp")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()

	paginator = Paginator(queryset_list, 25) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list": queryset,
		"Login": "Login",
		"page_request_var": page_request_var
	}
	#if request.user.is_authenticated():
	#	context = {
	#		"Login":"Login"
	#	}
	#else:
	#	context = {
	#		"Login":"LogOut"
	#	}
	return render(request, "html/post_list.html", context)


	

def post_update(request, id=None):
	#if request.user.is_staff or not request.user.is_superuser:
	#	raise Http404
	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tag='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"Login": "Login",
		"form":form,
		"instance": instance,
	}
	return render(request, "html/post_form.html", context)

def post_delete(request, id=None):
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "제거되었습니다.")
	return redirect("Main:list")
