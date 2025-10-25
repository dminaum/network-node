from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status

from network_node.models import NetworkNode


@pytest.mark.django_db
class TestNetworkNodeAPI:
    def test_list_nodes_unauthenticated(self, api_client):
        """Неаутентифицированный доступ запрещен"""
        url = reverse("networknode-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_nodes_inactive_user(self, api_client, inactive_user):
        """Неактивный пользователь не имеет доступа"""
        api_client.force_authenticate(user=inactive_user)
        url = reverse("networknode-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_nodes_authenticated(self, authenticated_client, factory_node):
        """Аутентифицированный пользователь получает список"""
        url = reverse("networknode-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_create_node(self, authenticated_client):
        """Тест создания узла"""
        url = reverse("networknode-list")
        data = {
            "name": "Новый завод",
            "node_type": NetworkNode.FACTORY,
            "email": "newfactory@test.com",
            "country": "Россия",
            "city": "Казань",
            "street": "Баумана",
            "house_number": "5",
            "debt": "0.00",
        }
        response = authenticated_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert NetworkNode.objects.filter(name="Новый завод").exists()

    def test_update_node_debt_forbidden(self, authenticated_client, retail_node):
        """Тест запрета обновления поля debt через API"""
        url = reverse("networknode-detail", kwargs={"pk": retail_node.pk})
        original_debt = retail_node.debt
        data = {
            "name": retail_node.name,
            "node_type": retail_node.node_type,
            "email": retail_node.email,
            "country": retail_node.country,
            "city": retail_node.city,
            "street": retail_node.street,
            "house_number": retail_node.house_number,
            "debt": "0.00",  # Попытка обнулить задолженность
        }
        response = authenticated_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK

        retail_node.refresh_from_db()
        assert retail_node.debt == original_debt  # Задолженность не изменилась

    def test_filter_by_country(self, authenticated_client, factory_node, retail_node):
        """Тест фильтрации по стране"""
        url = reverse("networknode-list")
        response = authenticated_client.get(url, {"country": "Россия"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 2

    def test_delete_node(self, authenticated_client, factory_node):
        """Тест удаления узла"""
        url = reverse("networknode-detail", kwargs={"pk": factory_node.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not NetworkNode.objects.filter(pk=factory_node.pk).exists()


@pytest.mark.django_db
class TestPermissions:
    def test_active_employee_permission(self, authenticated_client):
        """Активный сотрудник имеет доступ"""
        url = reverse("networknode-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_inactive_employee_no_permission(self, api_client, inactive_user):
        """Неактивный сотрудник не имеет доступа"""
        api_client.force_authenticate(user=inactive_user)
        url = reverse("networknode-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
