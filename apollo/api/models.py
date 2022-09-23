from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The email must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    email = models.EmailField(_('email address'), max_length=100, unique=True, blank=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def get_username(self):
        return self.__str__()


class StoreCurrency(models.TextChoices):
    ADA = "ADA"
    BTC = "BTC"
    ETH = "ETH"
    XRP = "XRP"
    XMR = "XMR"
    BNB = "BNB"
    LTC = "LTC"
    DOGE = "DOGE"
    USDT = "USDT.ERC20"


class StoreTransactionStatus(models.TextChoices):
    CANCELLED = "CANCELLED"
    AWAITING_PAYMENT = "AWAITING_PAYMENT"
    AWAITING_CONFIRMATIONS = "AWAITING_CONFIRMATIONS"
    PAYMENT_COMPLETE = "PAYMENT_COMPLETE"


class StoreTransaction(models.Model):
    id = models.TextField(unique=True, primary_key=True)
    tx_status = models.CharField(max_length=255, choices=StoreTransactionStatus.choices, default=StoreTransactionStatus.AWAITING_PAYMENT, null=False)
    currency = models.CharField(max_length=255, choices=StoreCurrency.choices, null=False)
    crypto_amount = models.DecimalField(max_digits=13, decimal_places=8)
    exchange_rate = models.DecimalField(max_digits=6, decimal_places=6)
    receiving_address = models.TextField(max_length=64)
    confirmations_needed = models.IntegerField(max_length=3, default=10)
    received_at = models.DateTimeField(null=True, blank=True)
    received_amount = models.IntegerField(max_length=3, default=0, null=False)
    received_confirmations = models.IntegerField(max_length=3, default=0, null=False)
    destination_tag = models.TextField(max_length=64, null=True, blank=False)
    qr_code_url = models.TextField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=False)
    last_updated = models.DateTimeField(auto_now_add=True)
    gift_card = models.TextField(max_length=255, null=True, blank=False)


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class StoreVariables(SingletonModel):
    extra_credit_enabled = models.BooleanField(default=False)
    extra_credit_percentage = models.FloatField(default=0.00)
