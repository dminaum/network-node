from django.contrib import admin
from django.utils.html import format_html

from .models import NetworkNode, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date")
    search_fields = ("name", "model")


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    """Admin action для очистки задолженности"""
    queryset.update(debt=0)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "node_type",
        "city",
        "supplier_link",
        "debt",
        "hierarchy_level",
        "created_at",
    )
    list_filter = ("city",)
    search_fields = ("name", "city", "country")
    actions = [clear_debt]
    readonly_fields = ("created_at", "hierarchy_level")

    fieldsets = (
        ("Основная информация", {"fields": ("name", "node_type", "supplier")}),
        ("Контактные данные", {"fields": ("email", "country", "city", "street", "house_number")}),
        ("Продукты и финансы", {"fields": ("products", "debt")}),
        (
            "Системная информация",
            {"fields": ("created_at", "hierarchy_level"), "classes": ("collapse",)},
        ),
    )

    filter_horizontal = ("products",)

    def supplier_link(self, obj):
        """Ссылка на поставщика"""
        if obj.supplier:
            url = f"/admin/network/networknode/{obj.supplier.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = "Поставщик"
