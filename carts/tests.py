from django.test import TestCase
from django.urls import reverse

from category.models import Category
from store.models import Product, Variation
from .models import CartItem


class CartQuantityTests(TestCase):
    def setUp(self):
        category = Category.objects.create(category_name="Clothing", slug="clothing")
        self.product = Product.objects.create(
            product_name="Blue Shirt",
            slug="blue-shirt",
            price=25,
            images="blue-shirt.jpg",
            stock=10,
            category=category,
        )
        self.color = Variation.objects.create(
            product=self.product,
            variation_category="color",
            variation_value="Blue",
        )
        self.size = Variation.objects.create(
            product=self.product,
            variation_category="size",
            variation_value="Medium",
        )

    def test_cart_plus_increments_same_variation_item(self):
        add_url = reverse("add_cart", args=[self.product.id])
        self.client.session.save()
        self.client.post(add_url, {"color": "blue", "size": "medium"})

        cart_page = self.client.get(reverse("cart"))
        self.assertRegex(
            cart_page.content.decode(),
            r'name\s*=\s*"color"\s+value\s*=\s*"blue"',
        )
        self.assertRegex(
            cart_page.content.decode(),
            r'name\s*=\s*"size"\s+value\s*=\s*"medium"',
        )

        self.client.post(add_url, {"color": "blue", "size": "medium"})

        cart_item = CartItem.objects.get(product=self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertCountEqual(
            cart_item.variations.all(),
            [self.color, self.size],
        )
        self.assertEqual(CartItem.objects.filter(product=self.product).count(), 1)
