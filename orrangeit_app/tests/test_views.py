from random import randint, choice

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from PIL import Image
import tempfile
from orrangeit_app.models import *

IMAGES = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg', '10.jpg']


class TestViews(TestCase):

    def setUp(self):
        #TODO: разбраться с ошибкой 302 модели EventInfo
        def create_image():
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                image = Image.new('RGB', (200, 200), 'white')
                image.save(f, 'PNG')

            return open(f.name, mode='rb')

        self.user = User(
            first_name='sasha',
            username='sasha',
            email='sasha@sasha.com'
        )
        self.user.save()
        self.tag = Tag.objects.create(tag='test')
        self.event1 = EventInfo(
                event_name='event_name',
                event_author=self.user,
                event_description='event_description',
                image=choice(IMAGES),
                event_people_needed=randint(0, 100)

            )
        event_id = self.event1.id
        self.client = Client()
        self.feed_url = reverse('feed_page')
        self.index_url = reverse('index')
        self.search_url = reverse('search_results')
        self.event_page_url = reverse('event_page', kwargs={'event_id':1})

    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_event_page_GET(self):
        response = self.client.get(self.event_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_page.html')

    def test_feed_GET(self):
        #FIXME:error 302
        response = self.client.get(self.feed_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_search_GET(self):
        #FIXME:error 302
        response = self.client.get(self.search_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('search_results.html')
