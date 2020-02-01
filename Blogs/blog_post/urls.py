from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('', views.blog_post_list),
    path('search', views.search_blog),
    path('create/comment/<str:slug>', views.add_comment),
    path('del_comment/<str:del_slug>/<int:del_id>/delete', views.blog_comm_delete),
    path('contact', views.contact_page),
    path('login', views.login_user),
    path('register', views.register_user),
    path('logout', views.logout_user),
    path('create/new/', views.blog_post_create),
    path('<str:slug>/edit', views.blog_post_update),
    path('<str:slug>/delete', views.blog_post_delete),
    path('<str:slug>/detail', views.blog_post_detail),
    # path('<str:username>/<str:number>/<str:password>/<str:email>', views.match_reg_otp),

    # path('<int:post_id>/', views.blog_details_id),
    # re_path('^(?P<post_id>\d+)/?$', views.blog_details_id),   # both are same but this is more used.
]
