from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path(r'ws/notifications/', consumers.NotificationsConsumer),
    re_path(r'ws/tg_group_creator/(?P<group_name>\w+)/$', consumers.TelegramConsumer)
]