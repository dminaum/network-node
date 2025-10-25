from decimal import Decimal

import pytest

from network_node.models import NetworkNode, Product


@pytest.mark.django_db
class TestProduct:
    def test_product_creation(self, sample_product):
        assert sample_product.name == "Ноутбук"
        assert sample_product.model == "X1 Carbon"
        assert str(sample_product) == "Ноутбук (X1 Carbon)"


@pytest.mark.django_db
class TestNetworkNode:
    def test_factory_creation(self, factory_node):
        assert factory_node.name == "Завод Электроника"
        assert factory_node.node_type == NetworkNode.FACTORY
        assert factory_node.hierarchy_level == 0
        assert factory_node.supplier is None

    def test_retail_hierarchy_level(self, retail_node):
        assert retail_node.hierarchy_level == 1
        assert retail_node.supplier is not None

    def test_debt_calculation(self, retail_node):
        assert retail_node.debt == Decimal("50000.00")
