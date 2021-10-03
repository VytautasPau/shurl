from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from time import time
from app_shurl.forms import UrlForm
from app_shurl.models import Url, UrlIndex


class UrlCreationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'lennon@thebeatles.com', 'testing123')

    # def tearDown(self):
    #     # Clean up after each test
    #     self.user.delete()

    def test_form(self):
        form = UrlForm({'url': "https://www.djangoproject.com/"})
        self.assertTrue(form.is_valid())

    def test_url_create(self):
        self.client.login(username="testuser", password="testing123")
        response = self.client.post(reverse("main"), data={'url': "https://www.djangoproject.com/"})

        self.assertIn(b"Your new short Url jas been generated:", response.content)

    def test_instance_creation(self):
        start_url_amount = len(Url.objects.all())
        start_index_amount = len(UrlIndex.objects.all())
        self.client.login(username="testuser", password="testing123")
        response = self.client.post(reverse("main"), data={'url': "https://www.djangoproject.com/"})
        amount2 = len(Url.objects.all())
        index_amount2 = len(UrlIndex.objects.all())
        self.assertEqual(start_url_amount+1, amount2)
        self.assertEqual(start_index_amount+1, index_amount2)

    def test_redirect(self):
        self.client.login(username="testuser", password="testing123")
        response = self.client.post(reverse("main"), data={'url': "https://www.djangoproject.com/"})
        # parse HTML data XD
        data = str(response.content)
        search_url = 'data-name="url"'
        pos = str(response.content).find(search_url)
        padd = len(search_url) + 7
        end_ind = data.find('"', pos+padd)
        url = data[pos+padd:end_ind]

        resp = self.client.get(url)
        destination = resp.get('location')
        self.assertEqual(destination, "https://www.djangoproject.com/")

    def test_redirect_error(self):
        self.client.login(username="testuser", password="testing123")
        response = self.client.post(reverse("main"), data={'url': "https://www.djangoproject.com/"})
        # parse HTML data XD
        data = str(response.content)
        search_url = 'data-name="url"'
        pos = str(response.content).find(search_url)
        padd = len(search_url) + 7
        end_ind = data.find('"', pos+padd)
        url = data[pos+padd:end_ind]
        if url[-1] != 'a':
            url = url[:-1] + 'a'
        else:
            url = url[:-1] + 'b'
        resp = self.client.get(url)
        self.assertEqual(404, resp.status_code)

    def test_benchmark_create(self):  # jei testai savo overhead papildomo neprideda.
        self.client.login(username="testuser", password="testing123")
        start_url_amount = len(Url.objects.all())
        start_time = time()
        for i in range(10000):
            response = self.client.post(reverse("main"), data={'url': "https://www.djangoproject.com/"})
            # ~ 39 sec
        end_time = time()
        amount2 = len(Url.objects.all())
        self.assertEqual(start_url_amount+10000, amount2)
        print("url creation benchmark. 10000 urls generated in (seconds): ", end_time - start_time)

    def test_benchmark_get(self):  # jei testai savo overhead papildomo neprideda.
        self.client.login(username="testuser", password="testing123")
        response = self.client.post(reverse("main"), data={'url': "https://www.djangoproject.com/"})
        # parse HTML data XD
        data = str(response.content)
        search_url = 'data-name="url"'
        pos = str(response.content).find(search_url)
        padd = len(search_url) + 7
        end_ind = data.find('"', pos+padd)
        url = data[pos+padd:end_ind]
        start_time = time()
        for i in range(10000):
            resp = self.client.get(url)
            # ~30 sec.
        end_time = time()
        destination = resp.get('location')
        self.assertEqual(destination, "https://www.djangoproject.com/")
        print("url retrieval benchmark. 10000 urls returned in (seconds): ", end_time - start_time)
