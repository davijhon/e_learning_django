from django.urls import path 

from blog.views import (
	BlogPageView, 
	# SearchResultsListView, 
    # CategoryPageView,
	PostDetailView,
)


app_name = 'blog'
urlpatterns = [

 	path('blog/', BlogPageView.as_view(), name='blog'),
 	path('blog/<slug:slug>', PostDetailView.as_view(), name='blog_post_detail'),
 	# path('search/', SearchResultsListView.as_view(), name='search_results'),
	# path('category/<int:pk>', CategoryPageView.as_view(), name='category'),

]