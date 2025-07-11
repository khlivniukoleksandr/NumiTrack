from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from items.models import Coin, Banknote


class CoinTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        user2 = get_user_model().objects.create_user(
            username="other_user", password="other_password"
        )
        self.client.login(username="test_user", password="test_password")

        Coin.objects.create(name="1 cent",
                            description="test",
                            country="USA",
                            year=2020,
                            denomination="cent",
                            material="silver",
                            owner=self.user)
        Coin.objects.create(name="100 UAH",
                            description="100 UAH",
                            country="Ukraine",
                            year=1998,
                            denomination="Hryvnia",
                            material="gold",
                            owner=self.user)
        Coin.objects.create(name="10 cent",
                            description="test",
                            country="Great Britain",
                            year=1900,
                            denomination="cent",
                            material="bronze",
                            owner=self.user)


    def test_search_coin(self):
        response = self.client.get(reverse("items:my-coins") + "?name=cent&country=US&material=silver")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1 cent")
        self.assertNotContains(response, "100 UAH")
        self.assertNotContains(response, "10 cent")

    def test_order_coin_by_year(self):

        response = self.client.get(reverse("items:my-coins") + "?sort=year")
        self.assertEqual(response.status_code, 200)
        coins = list(response.context["coins"])
        self.assertEqual([coin.year for coin in coins], sorted([1900, 1998, 2020]))

    def test_update_coin_by_another_user(self):
        coin = Coin.objects.create(name="1 cent",
                                   description="test",
                                   country="USA",
                                   year=2020,
                                   denomination="cent",
                                   material="silver",
                                   owner=self.user)
        self.client.logout()
        self.client.login(username="other_user", password="other_password")
        url = reverse("items:coin-edit", kwargs={"pk": coin.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_coin_by_another_user(self):
        coin = Coin.objects.create(name="1 cent",
                                   description="test",
                                   country="USA",
                                   year=2020,
                                   denomination="cent",
                                   material="silver",
                                   owner=self.user)
        self.client.logout()
        self.client.login(username="other_user", password="other_password")
        url = reverse("items:coin-delete", kwargs={"pk": coin.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class BanknoteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        user2 = get_user_model().objects.create_user(
            username="other_user", password="other_password"
        )
        self.client.login(username="test_user", password="test_password")

        Banknote.objects.create(name="200 UAH",
                                description="200 UAH banknote",
                                country="Ukraine",
                                year=2005,
                                value="200 UAH",
                                owner=self.user)
        Banknote.objects.create(name="20 rupy",
                                description="20 dollars banknote",
                                country="India",
                                year=2015,
                                value="20 rupy",
                                owner=self.user)
        Banknote.objects.create(name="20 dollars",
                                description="20 dollars banknote",
                                country="Canada",
                                year=2013,
                                value="20 dollars",
                                owner=self.user)
        Banknote.objects.create(name="20 riel",
                                description="20 riel banknote",
                                country="Cambodia",
                                year=2024,
                                value="20 riel",
                                owner=self.user)

    def test_search_banknote(self):
        response = self.client.get(reverse("items:my-banknotes") + "?name=20&year=20&country=Ca")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "200 UAH")
        self.assertNotContains(response, "20 rupy")
        self.assertContains(response, "20 dollars")
        self.assertContains(response, "20 riel")

    def test_order_banknote_by_year(self):
        response = self.client.get(reverse("items:my-banknotes") + "?sort=year")
        self.assertEqual(response.status_code, 200)
        banknotes = list(response.context["banknotes"])
        self.assertEqual([banknote.year for banknote in banknotes], sorted([2005, 2013, 2015, 2024]))

    def test_update_banknote_by_another_user(self):
        banknote = Banknote.objects.create(name="1 dollar",
                                   description="test",
                                   country="USA",
                                   year=2020,
                                   value="cent",
                                   owner=self.user)
        self.client.logout()
        self.client.login(username="other_user", password="other_password")
        url = reverse("items:banknote-edit", kwargs={"pk": banknote.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_banknote_by_another_user(self):
        banknote = Banknote.objects.create(name="1 dollar",
                                   description="test",
                                   country="USA",
                                   year=2010,
                                   value="cent",
                                   owner=self.user)
        self.client.logout()
        self.client.login(username="other_user", password="other_password")
        url = reverse("items:banknote-delete", kwargs={"pk": banknote.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)