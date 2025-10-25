from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    """Модель продукта"""

    name = models.CharField(max_length=255, verbose_name="Название")
    model = models.CharField(max_length=255, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода на рынок")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    """Модель звена сети"""

    FACTORY = 0
    RETAIL = 1
    ENTREPRENEUR = 2

    NODE_TYPES = (
        (FACTORY, "Завод"),
        (RETAIL, "Розничная сеть"),
        (ENTREPRENEUR, "Индивидуальный предприниматель"),
    )

    name = models.CharField(max_length=255, verbose_name="Название")
    node_type = models.IntegerField(choices=NODE_TYPES, verbose_name="Тип звена")

    # Контакты
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=255, verbose_name="Улица")
    house_number = models.CharField(max_length=20, verbose_name="Номер дома")

    # Связи
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
        verbose_name="Поставщик",
    )

    products = models.ManyToManyField(
        Product, related_name="network_nodes", verbose_name="Продукты"
    )

    # Финансы
    debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        default=Decimal("0.00"),
        verbose_name="Задолженность перед поставщиком",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    @property
    def hierarchy_level(self):
        """Вычисление уровня в иерархии"""
        level = 0
        current = self
        while current.supplier:
            level += 1
            current = current.supplier
        return level

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"

    def __str__(self):
        return f"{self.name} (Уровень {self.hierarchy_level})"
