from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from catalog.models import Item
from .managers import CustomUserManager


class ShopUser(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(_('email address'), unique=True)

    first_name = models.CharField(default=None, null=True, blank=True, max_length=20)
    last_name = models.CharField(default=None, null=True, blank=True, max_length=20)
    phone_number = models.CharField(default=None, null=True, blank=True, max_length=20, )
    avatar = models.ImageField(default='/media/users/user.jpg', upload_to='users')
    send_news = models.BooleanField(default=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    objects = CustomUserManager()
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    def has_perm(self, perm, obj=None):
        return True

    def __str__(self):
        return self.username


class VarificationCode(models.Model):
    hash_key = models.CharField(max_length=6, unique=True, )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attempt_amount = models.IntegerField()

    def __str__(self):
        return self.hash_key


class FavoriteItem(models.Model):
    item = models.ForeignKey('catalog.Item', on_delete=models.CASCADE, )
    user = models.ForeignKey('ShopUser', on_delete=models.CASCADE)
