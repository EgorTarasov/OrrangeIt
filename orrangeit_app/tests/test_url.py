from django.test import SimpleTestCase
from django.urls import reverse, resolve
from orrangeit_app import views

IMAGES = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg', '10.jpg']

class TestUrl(SimpleTestCase):

    def test_url_index_resolved(self):
        url = reverse('index')

        self.assertEquals(resolve(url).func, views.index)

    def test_url_feed_page_resolved(self):
        url = reverse('feed_page')

        self.assertEquals(resolve(url).func, views.feed)

    def test_url_email_verification_resolved(self):
        url = reverse('email_verification')

        self.assertEquals(resolve(url).func, views.email_verification)

    def test_url_user_logout_resolved(self):
        url = reverse('user_logout')

        self.assertEquals(resolve(url).func, views.user_logout)

    '''def test_url_event_page_resolved(self):
        url = reverse('event_page', event_id = )

        self.assertEqual(resolve(url).func, views.event_page)
    def test_url_user_page_resolved(self):
        url = reverse('user_page')

        self.assertEqual(resolve(url).func, views.user_page)
    '''
    def test_url_search_results_resolved(self):
        url = reverse('search_results')

        self.assertEqual(resolve(url).func, views.search_view)
