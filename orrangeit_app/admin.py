from django.contrib import admin

from .models import EventInfo, Tag, ImagesGen

admin.site.register(EventInfo)
admin.site.register(Tag)
admin.site.register(ImagesGen)