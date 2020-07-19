
# Create your tests here.
from django.test import TestCase
from shopping_cart_api.models import Campaign, Coupon, ProductCategory, Product, Discount
from shopping_cart_api.business.shopping_cart import CartItem, ShoppingCart


class ShoppingCartTests(TestCase):
    shopping_cart: ShoppingCart
    product: Product
    category_with_campaign: ProductCategory
    campaign: Campaign
    coupon: Coupon

    @classmethod
    def setUpTestData(cls):
        # setup campaign
        cls.campaign = Campaign.objects.create(
            minimum_cart_items_quantity=3,
            discount_type=Discount.DISCOUNT_TYPE_RATE,
            discount_value=0.5)

        # setup categories
        parent = ProductCategory.objects.create()
        parent2 = ProductCategory.objects.create(parentProductCategory=parent)
        cls.category_with_campaign = ProductCategory.objects.create(
            parentProductCategory=parent2)
        cls.category_with_campaign.campaigns.add(cls.campaign)
        cls.category_with_campaign.save()

        # setup product
        cls.product = Product.objects.create(price=20, title="great product",
                                             category=cls.category_with_campaign)
        # setup shopping cart
        cls.shopping_cart = ShoppingCart()

        # setup coupon
        cls.coupon = Coupon(minimum_amount=10,
                            discount_type=Discount.DISCOUNT_TYPE_AMOUNT,
                            discount_value=10)

    def test_add_cart_item(self):
        quantity = 3
        cart_item = CartItem(self.product, quantity)
        self.shopping_cart.add_item(cart_item)

        self.assertEqual(
            len(self.shopping_cart.cart_items),
            1
        )
        self.assertEqual(self.shopping_cart.cart_items[0].product.id,
                         self.product.id)
        self.assertEqual(self.shopping_cart.cart_items[0].quantity,
                         quantity)

    def test_apply_coupon(self):
        self.assertEqual(self.shopping_cart.applied_coupon,
                         None)
        self.shopping_cart.apply_coupon(self.coupon)
        self.assertEqual(self.shopping_cart.applied_coupon, self.coupon)

    def test_get_total_amount_before_discounts(self):
        self.assertEqual(self.shopping_cart.get_total_amount_before_discounts(),
                         self.product.price * self.shopping_cart.cart_items[0].quantity)

    def test_get_campaign_discount(self):
        self.assertEqual(self.shopping_cart.get_campaign_discount(), 30)

    def test_get_coupon_discount(self):
        campaign_discounted = self.shopping_cart.get_total_amount_before_discounts() - \
            self.shopping_cart.get_campaign_discount()
        self.assertEqual(
            self.shopping_cart.get_coupon_discount(campaign_discounted),
            10
        )

    def test_get_total_amount_after_discounts(self):
        self.assertEqual(
            self.shopping_cart.get_total_amount_after_discounts(), (20*3)-(30+10))

    def test_get_number_of_unique_categories(self):
        self.assertEqual(
            self.shopping_cart.get_number_of_unique_categories(), 1
        )

    def test_get_number_of_unique_products(self):
        self.assertEqual(
            self.shopping_cart.get_number_of_unique_products(), 1
        )
