from decimal import Decimal

import pytest
from django.contrib.admin.sites import AdminSite

from network_node.admin import NetworkNodeAdmin, clear_debt
from network_node.models import NetworkNode


@pytest.mark.django_db
class TestAdminActions:
    def test_clear_debt_action(self, retail_node, factory_node):
        """Тест admin action для очистки задолженности"""
        assert retail_node.debt > 0

        queryset = NetworkNode.objects.filter(pk=retail_node.pk)
        clear_debt(None, None, queryset)

        retail_node.refresh_from_db()
        assert retail_node.debt == Decimal("0.00")

    def test_supplier_link(self, retail_node, factory_node):
        """Тест отображения ссылки на поставщика"""
        site = AdminSite()
        admin = NetworkNodeAdmin(NetworkNode, site)
        link = admin.supplier_link(retail_node)
        assert factory_node.name in link
        assert "/admin/" in link
