from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from items.forms import CustomCollectionForm
from items.models import Coin, Banknote


class FormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )

    def test_collection_creating_form(self):
        self.client.login(username="test_user", password="test_password")
        form_data = {
            "name": "test",
            "description": "test",
        }
        form = CustomCollectionForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], form_data["name"])

    def test_coin_creating_form(self):
        self.client.login(username="test_user", password="test_password")
        form_data = {
            "name": "10 UAH",
            "description": "Collection coin",
            "country": "Ukraine",
            "year": 2025,
            "denomination": "UAH",
            "material": "Neusilber"
        }
        response = self.client.post(reverse("items:coin-create"), data=form_data)
        self.assertEqual(response.status_code, 302)
        coin = Coin.objects.get(name="10 UAH")
        self.assertEqual(coin.owner, self.user)

    def test_banknote_creating_form(self):
        self.client.login(username="test_user", password="test_password")
        form_data = {
            "name": "20 UAH",
            "description": "Collection banknote",
            "country": "Ukraine",
            "year": 2017,
            "value": "UAH",
        }
        response = self.client.post(reverse("items:banknote-create"), data=form_data)
        self.assertEqual(response.status_code, 302)
        banknote = Banknote.objects.get(name="20 UAH")
        self.assertEqual(banknote.owner, self.user)
