from django.urls import path,include,re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from PittsTime import views

urlpatterns = [
    path('', views.login_action, name='login'),
    path('home',views.home_page, name="home"),
    path('spotify_login',views.spotify_login,name='spotify_login'),
    path('spotify_addUserInfo',views.spotify_addUserInfo,name='spotify_addUserInfo'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('timeline',views.my_timeline_action,name='timeline'),
    # path('gallery',views.my_gallery_action,name='gallery'),
    path('interest',views.myinterest_action, name='interest'),
    path('blog-detail/<int:id>', views.blog_detail_action, name='blog-detail'),
    path('tag/<int:id>', views.one_interest, name='tag'),
    path('tag_myinterest/<int:id>', views.one_interest, name='tag_myinterest'),
    path('add-location', views.add_location, name='add-location'),
    path('add-comment', views.add_comment, name='add-comment'),
    path('createBlog',views.createBlog_action,name='createBlog'),
    path('manageBlog',views.manageBlog_action,name='manageBlog'),
    path('blog-delete/<int:id>',views.blog_delete_action,name='blog-delete'),
    path('blog-edit/<int:id>',views.blog_edit_action,name='blog-edit'),
    path('add-track',views.add_track,name='add_track'),
    path('createBlog_next', views.next_action, name='createBlog_next'),
    path('spotify', views.spotify, name='spotify'),
    path('spotify/callback/q', views.spotify_callback, name ='callback'),
    path('search_track', views.search_track, name='search_track'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('myprofile',views.myprofile,name='myprofile'),
    path('updateProfile',views.updateProfile,name='updateProfile'),
    path('other_profile/<int:id>',views.other_profile,name='other_profile'),
    path('photo/<int:id>',views.get_photo,name='photo'),
    path('add_interest/<int:id>',views.add_interest,name='add_interest'),
    path('delete_interest/<int:id>',views.delete_interest,name='delete_interest'),
    path('add_interest_profile/<int:id>',views.add_interest,name='add_interest_profile'),
    path('delete_interest_profile/<int:id>',views.delete_interest,name='delete_interest_profile'),
    path('add_interest_myinterest/<int:id>',views.add_interest,name='add_interest_myinterest'),
    path('delete_interest_myinterest/<int:id>',views.delete_interest,name='delete_interest_myinterest'),
]
