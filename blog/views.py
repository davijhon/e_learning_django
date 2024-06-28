from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
# from django.db.models import Q
from django.views.generic import ( 
	View, 
	TemplateView, 
	ListView, 
	DetailView 
)

from blog.models import (
	Post, 
	Category, 

)



class BlogPageView(ListView):
	model = Post
	template_name = 'blog/blog.html'
	context_object_name = 'posts'
	paginate_by = 2

	def get_context_data(self, **kwargs):
		categories = Category.objects.all()
		ctx = super().get_context_data(**kwargs)
		ctx['categories'] = categories
		return ctx


# class CategoryPageView(View):

# 	def get(self, request, pk, *args, **kwargs):
# 		categories = Category.objects.all()
# 		posts = Post.objects.filter(categoria_id=pk)
# 		context = {
# 			'posts': posts,
# 			'categories': categories,
# 		}
# 		print(posts)
# 		return render(request, 'blog/category.html', context)


# class SearchResultsListView(ListView):
# 	model = Post
# 	context_object_name = 'post_list'
# 	template_name = 'blog/search.html'
# 	paginate_by = 3

# 	def get_queryset(self):
# 		query = self.request.GET.get('q')
# 		return Post.objects.filter(
# 			Q(titulo__icontains=query) | Q(autor__nombre__icontains=query)
# 		)


class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/blog_post.html'

	def get_context_data(self, **kwargs):
		categories = Category.objects.all()
		ctx = super().get_context_data(**kwargs)
		ctx['categories'] = categories
		return ctx
