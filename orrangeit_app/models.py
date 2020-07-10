from django.db import models
import datetime
from tinymce.models import HTMLField
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import AbstractUser


MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


class User(AbstractUser):
    user_avatar = models.ImageField(
        upload_to="uploads",
        blank=True
    )

    def __str__(self):
        return self.username

    @property
    def group_name(self):
        return "user_%s" % self.id


class ImagesGen(models.Model):
    image = models.ImageField(
        upload_to="uploads",
        blank=True
    )


image_storage = FileSystemStorage(
    # Physical file location ROOT
    location=u'{0}/my_sell/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url=u'{0}my_sell/'.format(settings.MEDIA_URL),
)


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/my_sell/picture/<filename>
    return u'picture/{0}'.format(filename)


class Tag(models.Model):
    tag = models.CharField(max_length=64, default='')


class GalleryImage(models.Model):
    image = models.ImageField(
        upload_to='gallery_images_directory',
        null=True,
        blank=True,
        storage=image_storage
    )


class EventInfo(models.Model):
    gallery = models.ManyToManyField(GalleryImage)

    event_tags = models.ManyToManyField(Tag)

    event_participants = models.ManyToManyField(
        User,
        related_name='event_participants',
        default=1
    )

    event_name = models.CharField(
        max_length=128,
        default=""
    )
    event_description = HTMLField(
        max_length=2048,
        default=""
    )

    event_begin = models.DateTimeField(
        default=datetime.datetime.now
    )

    event_end = models.DateTimeField(
        default=datetime.datetime.now
    )

    event_address = models.CharField(
        max_length=128,
        default=" "
    )

    event_people_needed = models.IntegerField(
        default=-1,
        auto_created=True
    )

    event_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_author'
    )

    is_event_active = models.BooleanField(
        default=True
    )

    telegram_chat = models.CharField(
        max_length=128,
        default=''
    )

    image = models.ImageField(
        upload_to='image_directory_path',
        null=True,
        blank=True,
        storage=image_storage
    )

    is_repeated = models.BooleanField(
        null=True,
        default=False
    )

    repeated_period = models.IntegerField(
        default=7,
        null=True
    )

    def check_if_repeated(self):
        if self.is_repeated:
            if datetime.datetime.now() > self.event_end():
                year, month, day, hour, minutes = self.event_begin.year,  self.event_begin.month, self.event_begin.day, self.event_begin.hour, self.event_begin.minutes
                day += 7
                if day > MONTH[month-1]:
                    day = day - MONTH[month-1]
                    month += 1
                if month > 12:
                    month, year = 1, year + 1
                new_begin_date = datetime.datetime(
                    year=self.event_begin.year,
                    month=self.event_begin.month,
                    day=day,
                    hour=hour,
                    minute=minutes
                )
                self.event_begin = new_begin_date
                year, month, day, hour, minutes = self.event_end.year, self.event_end.monthm, self.event_end.day, self.event_end.hour, self.event_end.minutes
                day += 7
                if day > MONTH[month-1]:
                    day = day - MONTH[month-1]
                    month += 1
                if month > 12:
                    month, year = 1, year + 1

                new_end_date = datetime.datetime(year=self.event_end.year, month=self.event_end.month, day=day)
                self.event_end = new_end_date
                self.save()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=512)
    event_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    '''
    # add like functuion
    def add_like(self):
        self.event_likes += 1;
        self.save()

    # add comment function
    def add_comment(self, comment):
        pass
    '''


class Like(models.Model):
    user_liked_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_like = models.DateTimeField(auto_now_add=True)
    event_like_id = models.IntegerField()


class Notify(models.Model):
    user_notify_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    event_notify_id = models.IntegerField()
    status = models.BooleanField(default=True)
    day_time = models.IntegerField()
    event_notify_name = models.CharField(max_length=128, default="")

