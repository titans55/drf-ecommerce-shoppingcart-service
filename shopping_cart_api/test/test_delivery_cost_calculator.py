
# Create your tests here.
from django.test import TransactionTestCase
from shopping_cart_api.models import ProductCategory, Product
from shopping_cart_api.business.shopping_cart import CartItem, ShoppingCart
from shopping_cart_api.business.delivery_cost_calculator import DeliveryCostCalculator
from decimal import Decimal


class TestDeliveryCostCalculatorTests(TransactionTestCase):
    shopping_cart: ShoppingCart
    delivery_cost_calculator: DeliveryCostCalculator

    def setUp(self):
        # setup delivery cost calculator
        self.delivery_cost_calculator = DeliveryCostCalculator(
            Decimal(5), Decimal(2), Decimal(2.99)
        )

        # setup categories (2 deliveries)
        category = ProductCategory(id=1)
        category2 = ProductCategory(id=2)

        # setup product (3 products)
        product = Product(id=1, category=category)
        product2 = Product(id=2, category=category2)
        product3 = Product(id=3, category=category2)

        # setup shopping cart
        self.shopping_cart = ShoppingCart()
        self.shopping_cart.add_item(CartItem(product, 3))
        self.shopping_cart.add_item(CartItem(product2, 1))
        self.shopping_cart.add_item(CartItem(product3, 2))

    def test_calculate_for(self):
        self.assertEqual(
            self.delivery_cost_calculator.calculate_for(self.shopping_cart),
            Decimal(5) * 2 + Decimal(2) * 3 + Decimal(2.99)
        )
