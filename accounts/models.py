from statistics import mode
import django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager

USER_STATUS = [
    (0, 'No Status'),
    (1, 'PENDING'),
    (2, 'APPROVED'),
    (3, 'REJECTED'),
]

class UserPermissions(models.Model):
    """User permissions model."""

    permission = models.CharField(_("Permission"), max_length=255, unique=True)


    def __str__(self):
        if self.permission:
            return self.permission
        return "No Permission"


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """ Custom User model
    """

    email = LowercaseEmailField(_('email address'), unique=True)
    full_name = models.CharField(_('Full Name'),max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    #status = models.IntegerField(_('User Status'), default=USER_STATUS[0][0], choices=USER_STATUS)
    custom_permissions = models.ManyToManyField(UserPermissions, blank=True)
    created_by = models.IntegerField(_('Created By'), default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.email:
            return self.email
        else:
            return "No Email Address"

    
    @staticmethod
    def get_user_by_email(email):
        try:
            return CustomUser.objects.get(email=email)
        except:
            return None


class UserProfile(models.Model):
    """ User Profile model. """

    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, related_name="user_profile")
    address = models.CharField(max_length=1000, default="", blank=True, null=True)
    phone = models.CharField(max_length=255, blank = True, null=True)
    photo = models.ImageField(_("Profile Photo"), upload_to="userphotos", blank= True, null=True)

    def __str__(self):
        if self.user is not None:
            return self.user.email
        else:
            return "Anonimus User"