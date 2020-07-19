from typing import List
from shopping_cart_api.models import Product, ProductCategory, Coupon
from decimal import Decimal


class CartItem:
    product: Product
    quantity: int

    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity


CartItems = List[CartItem]


class ShoppingCart:
    cart_items: CartItems
    applied_coupon: Coupon

    def __init__(self):
        self.cart_items = []
        self.applied_coupon = None

    def add_item(self, cart_item: CartItem) -> None:
        self.cart_items.append(cart_item)

    def apply_coupon(self, coupon: Coupon) -> None:
        self.applied_coupon = coupon

    def get_total_amount_before_discounts(self) -> Decimal:
        total_cost_before_discounts: Decimal = Decimal(0)
        for cart_item in self.cart_items:
            total_cost_before_discounts += cart_item.quantity * cart_item.product.price
        return total_cost_before_discounts

    def get_campaign_discount(self) -> Decimal:
        campaign_discount: Decimal = Decimal(0)
        for cart_item in self.cart_items:
            category: ProductCategory = cart_item.product.category
            while category:
                for campaign in category.campaigns.all():
                    discount = campaign.get_discount(
                        cart_item.quantity,
                        self.get_total_amount_before_discounts()
                    )
                    campaign_discount = discount if discount > campaign_discount else campaign_discount
                category = category.parentProductCategory
        return campaign_discount

    def get_coupon_discount(self, cost: Decimal) -> Decimal:
        coupon_discount: Decimal = Decimal(0)
        if self.applied_coupon:
            coupon_discount = self.applied_coupon.get_discount(
                len(self.cart_items),
                cost
            )
        return coupon_discount

    def get_total_amount_after_discounts(self) -> Decimal:
        total_amount_before_discounts = self.get_total_amount_before_discounts()

        campaign_discounted = total_amount_before_discounts - self.get_campaign_discount()
        coupon_discont = self.get_coupon_discount(campaign_discounted)

        return total_amount_before_discounts - (campaign_discounted + coupon_discont)

    def get_number_of_unique_products(self) -> int:
        product_ids = []
        for cart_item in self.cart_items:
            product_ids.append(cart_item.product.id)
        return len(set(product_ids))

    def get_number_of_unique_categories(self) -> int:
        category_ids = []
        for cart_item in self.cart_items:
            category_ids.append(cart_item.product.category.id)

        return len(set(category_ids))
