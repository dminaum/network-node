from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from network_node.models import NetworkNode, Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def active_user(db):
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123", is_active=True
    )


@pytest.fixture
def inactive_user(db):
    return User.objects.create_user(
        username="inactiveuser",
        email="inactive@example.com",
        password="testpass123",
        is_active=False,
    )


@pytest.fixture
def authenticated_client(api_client, active_user):
    api_client.force_authenticate(user=active_user)
    return api_client


@pytest.fixture
def sample_product(db):
    return Product.objects.create(name="Ноутбук", model="X1 Carbon", release_date="2024-01-15")


@pytest.fixture
def factory_node(db, sample_product):
    node = NetworkNode.objects.create(
        name="Завод Электроника",
        node_type=NetworkNode.FACTORY,
        email="factory@electronics.com",
        country="Россия",
        city="Москва",
        street="Ленина",
        house_number="1",
        debt=Decimal("0.00"),
    )
    node.products.add(sample_product)
    return node


@pytest.fixture
def retail_node(db, factory_node, sample_product):
    node = NetworkNode.objects.create(
        name="Сеть DNS",
        node_type=NetworkNode.RETAIL,
        email="dns@electronics.com",
        country="Россия",
        city="Санкт-Петербург",
        street="Невский",
        house_number="10",
        supplier=factory_node,
        debt=Decimal("50000.00"),
    )
    node.products.add(sample_product)
    return node
