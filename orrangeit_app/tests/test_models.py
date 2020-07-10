from django.test import TestCase
from orrangeit_app.models import *
from random import randint, choice

IMAGES = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg', '10.jpg']


class TestModels(TestCase):

    def setUp(self):
        self.user = User(
            first_name='sasha',
            username='sasha',
            email='sasha@sasha.com'
        )
        self.user.save()
        self.event1 = EventInfo(
            event_name='event_name',
            event_author=self.user,
            event_description='event_description',
            image=choice(IMAGES),
            event_people_needed=randint(0, 100)

        )
        self.event1.save()
        self.event1.event_participants.add(User.objects.get(pk=self.user.pk))
        self.img = self.event1.image

    def test_event_chat_created(self):
        self.assertEqual(self.event1.telegram_chat,'')

    def test_event_participants(self):
        self.assertEqual(self.event1.event_participants.get(pk=self.user.pk), self.user)

    def test_all_field_acces(self):
        event = EventInfo.objects.get(pk=self.event1.pk)

        self.assertNotEqual(self.event1.event_begin, None)
        self.assertNotEqual(self.event1.event_end, None)
        self.assertEqual(self.event1.is_event_active, True)
        self.assertEqual(self.event1.event_name, 'event_name')
        self.assertEqual(self.event1.event_description, 'event_description')
        self.assertEqual(self.event1.image, self.img)