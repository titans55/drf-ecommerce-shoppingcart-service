from .shopping_cart import ShoppingCart
from decimal import Decimal


class DeliveryCostCalculator:
    cost_per_delivery: Decimal
    cost_per_product: Decimal
    fixed_cost: Decimal

    def __init__(self, cost_per_delivery: Decimal, cost_per_product: Decimal, fixed_cost):
        self.cost_per_delivery = cost_per_delivery
        self.cost_per_product = cost_per_product
        self.fixed_cost = fixed_cost

    def calculate_for(self, cart: ShoppingCart) -> Decimal:
        number_of_deliveries = cart.get_number_of_unique_categories()
        number_of_products = cart.get_number_of_unique_products()
        return (self.cost_per_delivery * number_of_deliveries) \
            + (self.cost_per_product * number_of_products) \
            + self.fixed_cost
