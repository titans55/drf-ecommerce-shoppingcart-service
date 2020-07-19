# Create your tests here.
from django.test import TestCase
from decimal import Decimal
from shopping_cart_api.models import Campaign, Coupon, Discount


class CouponDiscountTests(TestCase):

    def test_coupon_applicability(self):
        coupon = Coupon(minimum_amount=10)
        self.assertEqual(coupon.is_applicable(0, Decimal(11)), True)
        self.assertEqual(coupon.is_applicable(0, Decimal(10)), True)
        self.assertEqual(coupon.is_applicable(0, Decimal(9)), False)

    def test_rate_discount_coupon(self):
        discount_value = Decimal(0.2)
        rate_coupon = Coupon(
            minimum_amount=15, discount_type=Discount.DISCOUNT_TYPE_RATE, discount_value=discount_value)

        self.assertEqual(
            rate_coupon.get_discount(1, Decimal(100)),
            100 * discount_value
        )
        self.assertEqual(rate_coupon.get_discount(1, Decimal(10)), 0)
        self.assertEqual(rate_coupon.get_discount(
            1, Decimal(20)), 20 * discount_value)

    def test_amount_discount_coupon(self):
        discount_value, minimum_amount = Decimal(10), Decimal(40)
        amount_coupon = Coupon(
            minimum_amount=minimum_amount, discount_type=Discount.DISCOUNT_TYPE_AMOUNT, discount_value=discount_value)

        self.assertEqual(
            amount_coupon.get_discount(1, Decimal(100)),
            discount_value
        )
        self.assertEqual(
            amount_coupon.get_discount(1, minimum_amount),
            discount_value
        )
        self.assertEqual(
            amount_coupon.get_discount(1, minimum_amount-1),
            0
        )


class CampaignDiscountTests(TestCase):

    def test_compaign_applicability(self):
        minimum_cart_items_quantity = 5
        campaign = Campaign(
            minimum_cart_items_quantity=minimum_cart_items_quantity)

        self.assertEqual(campaign.is_applicable(
            minimum_cart_items_quantity+1, Decimal(0)), True)
        self.assertEqual(campaign.is_applicable(
            minimum_cart_items_quantity, Decimal(0)), True)
        self.assertEqual(campaign.is_applicable(
            minimum_cart_items_quantity-1, Decimal(0)), False)

    def test_rate_campaign(self):
        discount_value, minimum_cart_items_quantity = Decimal(0.2), 5
        rate_campaign = Campaign(
            minimum_cart_items_quantity=minimum_cart_items_quantity,
            discount_type=Discount.DISCOUNT_TYPE_RATE,
            discount_value=discount_value
        )

        self.assertEqual(
            rate_campaign.get_discount(
                minimum_cart_items_quantity+1, Decimal(100)),
            100 * discount_value
        )
        self.assertEqual(
            rate_campaign.get_discount(
                minimum_cart_items_quantity, Decimal(100)),
            100 * discount_value
        )
        self.assertEqual(
            rate_campaign.get_discount(
                minimum_cart_items_quantity-1, Decimal(100)),
            0
        )

    def test_amount_campaign(self):
        discount_value, minimum_cart_items_quantity = Decimal(10), 5
        amount_campaign = Campaign(
            minimum_cart_items_quantity=minimum_cart_items_quantity,
            discount_type=Discount.DISCOUNT_TYPE_AMOUNT,
            discount_value=discount_value
        )

        self.assertEqual(
            amount_campaign.get_discount(
                minimum_cart_items_quantity+1, Decimal(100)),
            discount_value
        )
        self.assertEqual(
            amount_campaign.get_discount(
                minimum_cart_items_quantity, Decimal(100)),
            discount_value
        )
        self.assertEqual(
            amount_campaign.get_discount(
                minimum_cart_items_quantity-1, Decimal(100)),
            0
        )
