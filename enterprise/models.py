from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

from django.db import models


# Create your managers here.abs
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password
        )
        user.user_id = str(uuid.uuid4())
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Create your models here.


class User(AbstractUser):
    last_login = models.DateTimeField(
        verbose_name="Last Login", blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=120, null=True)
    user_id = models.CharField(max_length=120, null=True)
    first_name = models.CharField(max_length=120, null=True)
    last_name = models.CharField(max_length=120, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_archived = models.CharField(max_length=10, default=False)
    date_joined = models.DateTimeField(
        verbose_name="Date Joined", auto_now_add=True)
    email = models.EmailField(
        verbose_name="Email address", max_length=100, unique=True)
    phone = models.CharField(
        verbose_name="Phone Number", max_length=20, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

    def has_perm(perm, obj=None):
        return True

    class Meta:
        ordering = ['id']


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    street = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    county = models.CharField(max_length=50, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    postal_address = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"Address for {self.user.username}"

    class Meta:
        # managed = True
        # verbose_name = 'ModelName'
        verbose_name_plural = 'Addresses'


class Loan(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True)


class MonthlyInstallment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    installment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)


class LoanPayment(models.Model):
    installment = models.ForeignKey(
        MonthlyInstallment, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True)


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    transaction_date = models.DateTimeField()

    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description = models.TextField(default='')


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('cash_on_delivery', 'Cash on Delivery'),
        ('MPESA', 'MPESA'),
        ('paypal', 'PayPal'),
    )
    order_code = models.CharField(max_length=255, unique=True, blank=True)
    confirmed = models.BooleanField(default=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    order_date = models.DateTimeField(
        verbose_name='Date of order', auto_now_add=True, blank=True)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(
        max_length=30, choices=PAYMENT_METHOD_CHOICES, default='mpesa')
    shipping_address = models.TextField(blank=True)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)

    def add_order_item_to_order(self, product, quantity, price):
        order_item = OrderItem.objects.create(
            order=self,
            product=product,
            quantity=quantity,
            price=price
        )
        return order_item

    def total_cost(self):
        return sum([oi.subtotal() for oi in self.orderitem_set.all()])

    def __str__(self):
        return f"Order #{self.id}: {self.order_code}"

    class Meta:
        ordering = ['id']


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    pc_code = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    p_code = models.CharField(max_length=255, null=True)
    description = models.TextField(max_length=255, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True)
    image = models.ImageField(upload_to='products', blank=True)
    quantity = models.IntegerField(default=0, blank=True)
    brand = models.CharField(max_length=255, null=True)
    categories = models.ManyToManyField(ProductCategory)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True)

    def subtotal(self):
        return self.quantity * self.price

    # def update_quantity(self, quantity):
    #     self.quantity = self.quantity + quantity
    #     self.save()

    def __str__(self):
        return f"OrderItem #{self.id} for Order #{self.order.id}: {self.order.order_code}"


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50)
    ec_code = models.CharField(max_length=50, default=str(uuid.uuid4()))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'ExpenseCategories'


class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    e_code = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    staff = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=20)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"
