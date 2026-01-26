# import uuid
# from django.db import models
# from django.contrib.auth.models import (
#     AbstractBaseUser,
#     PermissionsMixin
# )
# from django.contrib.auth.base_user import BaseUserManager


# # =========================
# # USER MANAGER
# # =========================
# class UserManager(BaseUserManager):

#     def create_user(self, username, password=None, phone=None, **extra_fields):
#         if not username:
#             raise ValueError("Username is required")
#         if not phone:
#             raise ValueError("Phone number is required")
#         if not password:
#             raise ValueError("Password is required")

#         user = self.model(
#             username=username,
#             phone=phone,
#             **extra_fields
#         )
#         user.set_password(password)  # 🔐 hashed
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password, phone=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         extra_fields.setdefault("is_active", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True")

#         return self.create_user(
#             username=username,
#             password=password,
#             phone=phone,
#             **extra_fields
#         )


# # =========================
# # USER MODEL
# # =========================
# class User(AbstractBaseUser, PermissionsMixin):
#     user_id = models.UUIDField(
#         default=uuid.uuid4,
#         editable=False,
#         unique=True
#     )
#     username = models.CharField(
#         max_length=100,
#         unique=True
#     )
#     phone = models.CharField(
#         max_length=15,
#         unique=True
#     )

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     objects = UserManager()

#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = ["phone"]

#     def _str_(self):
#         return self.username
    


from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from datetime import datetime, timedelta
from django.utils import timezone 

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, phone=None, campaign_code=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        if not phone:
            raise ValueError("Phone number is required")
        if not password:
            raise ValueError("Password is required")

        user = self.model(
            username=username,
            phone=phone,
            campaign_code=campaign_code,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, phone=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)  # superuser verified by default

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, password, phone, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    campaign_code = models.CharField(max_length=50, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # phone verified

    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone"]

    def __str__(self):
        return self.username

    def set_otp(self, otp, expiry_minutes=5):
        self.otp_code = otp
        self.otp_expiry = datetime.now() + timedelta(minutes=expiry_minutes)
        self.save()

    def verify_otp(self, otp):
        from django.utils import timezone

        now = timezone.now()  # aware datetime

        otp_expiry = self.otp_expiry
        if timezone.is_naive(otp_expiry):
            otp_expiry = timezone.make_aware(otp_expiry, timezone.utc)

        if self.otp_code == otp and otp_expiry and otp_expiry > now:
            return True
        return False





