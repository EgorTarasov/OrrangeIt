from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from orrangeit_app import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('map/', login_required(views.CreateEventView.as_view()), name='map_page'),
    path('<int:event_id>/edit', views.EditEventView.as_view(), name='event_edit_page'),
    path('<int:pk>/delete', views.DeleteEventView.as_view(), name='delete_event'),
    path('feed/', views.feed, name='feed_page'),
    path('email_verification/', views.email_verification, name='email_verification'),
    path('logout/', views.user_logout, name='user_logout'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path('', include('django.contrib.auth.urls')),
    path('event/<int:event_id>', views.event_page, name='event_page'),
    path('profile/<str:username>', views.user_page, name='user_page'),
    url(r'^tinymce/', include('tinymce.urls')),
    path('search/', views.search_view, name='search_results'),
    path('tag_search/<int:tag_id>', views.search_tags, name='search_tags'),
    path('action_<int:action_type>_to_<int:event_id>', views.follow_unfollow_event, name='follow_unfollow')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
