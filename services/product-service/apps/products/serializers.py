from rest_framework import serializers
from .models import Category, Size, Product, ProductSize, ProductImage

class CategorySerializer(serializers.ModelSerializer):

    product_quantities = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'created_at', 'product_quantities')

    def get_product_quantities(self, obj):
        return obj.products.filter(is_active=True).count()

class SizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Size
        fields = ('id', 'name')

class ProductImageSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(use_url = True)
    
    class Meta:
        model = ProductImage
        fields = ('id', 'image')
    
class ProductCartSerializer(serializers.ModelSerializer):

    category = serializers.CharField(read_only=True)
    main_image = serializers.ImageField(read_only=True)
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'price', 'main_image', 'is_active', 'created_at')

class ProductSizeSerializer(serializers.ModelSerializer):

    size = serializers.CharField(read_only = True)
    is_in_stock = serializers.BooleanField(read_only = True)
    
    class Meta:
        model = ProductSize
        fields = ('id', 'size', 'stock_quantity', 'is_in_stock')
        
class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    product_sizes = ProductSizeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'category',
            'images',
            'product_sizes',
            'is_active',
            'created_at',
        )