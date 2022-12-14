from unittest import TestCase
from django.test import Client
from django.urls import reverse
from django.conf import settings
import json
import logging
import django_pytest
from companies.models import Company
import pytest
import inspect

if not settings.configured:
    settings.configure(django_pytest, DEBUG=True)

logger = logging.getLogger("testApi")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler = logging.FileHandler("testApi.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info("************")
logger.info("Starting testing...")
logger.info("************")


@pytest.mark.django_db
class BasiCompanyAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    def tearDown(self) -> None:
        pass


class TestGetCOmpanies(BasiCompanyAPITestCase):
    def test_zero_comapnies_return_empty_list(self) -> None:
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_success(self) -> None:
        test_company = Company.objects.create(name="XXXAAA")
        response = self.client.get(self.companies_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name", None), test_company.name)
        self.assertEqual(response_content.get("status", None), "Hiring")

        # test_company.delete()


@pytest.mark.django_db
class TestPostCompanies(BasiCompanyAPITestCase):
    def test_create_company_without_args(self) -> None:
        response = self.client.post(self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content).get("name", None)[0], "This field is required."
        )

    def test_create_existing_comapny_should_fail(self) -> None:
        Company.objects.create(name="Opel")
        response = self.client.post(self.companies_url, data={"name": "Opel"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content).get("name", None)[0],
            "company with this name already exists.",
        )

    def test_create_company_only_with_name(self) -> None:
        response = self.client.post(self.companies_url, data={"name": "BMW"})
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("name"), "BMW")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_comapny_with_layoffs_status_should_success(self) -> None:
        response = self.client.post(
            self.companies_url, data={"name": "Mercedes", "status": "Layoffs"}
        )
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("name"), "Mercedes")
        self.assertEqual(response_content.get("status"), "Layoffs")

    def test_create_company_with_wrong_status(self) -> None:
        response = self.client.post(
            self.companies_url, data={"name": "Audi", "status": "layoffs111"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("is not a valid ", str(response.content))
