from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from marketing.views import email_list_signup, access_list_signup
from posts.views import (
                        index, post, post_update, post_delete, 
                        post_create, blog, blog_by_category, blog_by_tag,
                        get_categories, search, about, access_tutorial_landing_page,
                        db_download,
                        )


urlpatterns = [
    path('im-gonna-pass-out/', admin.site.urls),
    path('', index, name='home-page'),
    path('blog/', blog, name='post-list'),
    path('categories/<category_slug>', blog_by_category, name='category-view'),
    path('categories/', get_categories, name='post-categories'),
    path('tag/<tag_slug>', blog_by_tag, name='tag-view'),
    path('about/', about, name='about-page'),
    path('search/', search, name='search'),
    path('subscribe/', email_list_signup, name='subscribe'),
    path('employee-management-timeclock-access-database/', access_tutorial_landing_page, name='access-database'),
    path('database-download/', db_download, name='db-download'),
    path('post/<pk>/', post, name='post-detail'),
    path('post/<pk>/update/', post_update, name='post-update'),
    path('post/<pk>/delete/', post_delete, name='post-delete'),
    path('create/', post_create, name='post-create'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)