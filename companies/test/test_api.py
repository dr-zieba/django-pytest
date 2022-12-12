from django.urls import reverse
from django.conf import settings
import json
import logging
import django_pytest
from companies.models import Company
import pytest

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

companies_url = reverse("companies-list")
# pytestmark will be applied to every function in file
pytestmark = pytest.mark.django_db


"""*********TEST GET COMPANIES**********"""


def test_zero_companies_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_company_exists_should_success(client) -> None:
    test_company = Company.objects.create(name="XXXAAA")
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name", None) == test_company.name
    assert response_content.get("status", None) == "Hiring"
    test_company.delete()


"""*********TEST POST COMPANIES**********"""


def test_create_company_without_args(client) -> None:
    response = client.post(companies_url)
    assert response.status_code == 400
    assert (
        json.loads(response.content).get("name", None)[0] == "This field is required."
    )


def test_create_existing_comapny_should_fail(client) -> None:
    Company.objects.create(name="Opel")
    response = client.post(companies_url, data={"name": "Opel"})
    assert response.status_code == 400
    assert (
        json.loads(response.content).get("name", None)[0]
        == "company with this name already exists."
    )


def test_create_company_only_with_name(client) -> None:
    response = client.post(companies_url, data={"name": "BMW"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name") == "BMW"
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_comapny_with_layoffs_status_should_success(client) -> None:
    response = client.post(
        companies_url, data={"name": "Mercedes", "status": "Layoffs"}
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name") == "Mercedes"
    assert response_content.get("status") == "Layoffs"


def test_create_company_with_wrong_status(client) -> None:
    response = client.post(companies_url, data={"name": "Audi", "status": "layoffs111"})
    assert response.status_code == 400
    assert "is not a valid " in str(response.content)
