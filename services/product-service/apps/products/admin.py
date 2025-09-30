from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from .models import Category, Size, Product, ProductImage, ProductSize

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ("image_preview",)
    fields = ("image", "image_preview")

    def image_preview(self, obj):
        if obj and getattr(obj, "image"):
            try:
                return format_html('<img src="{}" style="max-height:120px;"/>', obj.image.url)
            except Exception:
                return "(no preview)"
        return ""
    image_preview.short_description = "Preview"

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    fields = ("size", "stock_quantity")

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_active", "created_at", "total_stock")
    list_filter = ("category", "is_active",)
    search_fields = ("name", "description")
    inlines = (ProductImageInline, ProductSizeInline)
    readonly_fields = ("created_at",)
    actions = ("make_active", "make_inactive")

    def total_stock(self, obj):
        total = obj.product_sizes.aggregate(total=Sum("stock_quantity"))["total"] or 0
        return total
    total_stock.short_description = "Total stock"

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} product(s) marked as active")
    make_active.short_description = "Mark selected products as active"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} product(s) marked as inactive")
    make_inactive.short_description = "Mark selected products as inactive"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

class SizeAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image_tag")
    readonly_fields = ("image_tag",)

    def image_tag(self, obj):
        if obj and getattr(obj, "image"):
            try:
                return format_html('<img src="{}" style="max-height:80px;"/>', obj.image.url)
            except Exception:
                return "(no preview)"
        return ""
    image_tag.short_description = "Preview"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)