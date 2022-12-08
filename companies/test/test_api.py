from unittest import TestCase
from django.test import Client
from django.urls import reverse
import json

class TestGetCOmpanies(TestCase):
    def test_zero_comapnies_return_empty_list(self) -> None:
        client = Client()
        companies_url = 'http://127.0.0.1:8000/companies/'
        response = client.get(companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

