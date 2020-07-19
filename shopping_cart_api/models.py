from django.db import models
from django.urls import reverse
from abc import ABCMeta, abstractmethod
from decimal import Decimal


class AbstractModelMeta(ABCMeta, type(models.Model)):
    pass


class ABCModel(models.Model):
    __metaclass__ = AbstractModelMeta

    class Meta:
        abstract = True


class Discount(ABCModel):

    DISCOUNT_TYPE_RATE = 0
    DISCOUNT_TYPE_AMOUNT = 1
    DISCOUNT_TYPES = [
        (DISCOUNT_TYPE_RATE, 'Rate'),
        (DISCOUNT_TYPE_AMOUNT, 'Amount'),
    ]

    # Fields
    id = models.AutoField(primary_key=True)
    discount_type = models.IntegerField(
        default=DISCOUNT_TYPE_RATE,
        choices=DISCOUNT_TYPES
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True

    @abstractmethod
    def is_applicable(self, cart_items_quantity: int, cost: Decimal) -> bool:
        pass

    def get_discount(self, cart_items_quantity: int, cost: Decimal) -> Decimal:
        discount: Decimal = Decimal(0)
        if(self.is_applicable(cart_items_quantity, cost)):
            if(self.discount_type == Discount.DISCOUNT_TYPE_RATE):
                discount = cost * self.discount_value
            elif(self.discount_type == Discount.DISCOUNT_TYPE_AMOUNT):
                discount = self.discount_value

        discount = discount if discount <= cost else cost
        return discount


class Coupon(Discount):

    # Fields
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def is_applicable(self, cart_items_quantity: int, cost: Decimal) -> bool:
        return cost >= self.minimum_amount

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("shopping_cart_api_Coupon_detail", args=(self.id,))

    def get_update_url(self):
        return reverse("shopping_cart_api_Coupon_update", args=(self.id,))


class Campaign(Discount):

    # Fields
    minimum_cart_items_quantity = models.PositiveSmallIntegerField()

    def is_applicable(self, cart_items_quantity: int, cost: Decimal) -> bool:
        return cart_items_quantity >= self.minimum_cart_items_quantity

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("shopping_cart_api_Campaign_detail", args=(self.id,))

    def get_update_url(self):
        return reverse("shopping_cart_api_Campaign_update", args=(self.id,))


class ProductCategory(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)

    # Relationships
    parentProductCategory = models.ForeignKey(
        "shopping_cart_api.ProductCategory",
        on_delete=models.SET_NULL,
        related_name="sub_categories",
        null=True
    )
    campaigns = models.ManyToManyField("shopping_cart_api.Campaign")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("shopping_cart_api_ProductCategory_detail", args=(self.id,))

    def get_update_url(self):
        return reverse("shopping_cart_api_ProductCategory_update", args=(self.id,))


class Product(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=30)

    # Relationships
    category = models.ForeignKey(
        "shopping_cart_api.ProductCategory",
        on_delete=models.SET_NULL,
        related_name="products",
        null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("shopping_cart_api_Product_detail", args=(self.id,))

    def get_update_url(self):
        return reverse("shopping_cart_api_Product_update", args=(self.id,))
