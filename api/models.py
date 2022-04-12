from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import jwt
from datetime import datetime, timedelta
from django.conf import settings
# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self, username, email, password=None):
		if not username:
			raise TypeError("users must have a username")

		if not email:
			raise TypeError("users must have an eamil")

		user = self.model(username=username, email=self.normalize_email(email))
		user.set_password(password)
		user.save()
		return user 


	def create_superuser(self, username, eamil, password):

		if not password:
			raise TypeError("superusers must have a password")

		user = self.create_user(username, email, password)
		user.is_superuser = True
		user.is_staff = True
		user.is_active = True
		user.save()

		return user


class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(db_index=True, max_length=200,unique=True)
	email = models.EmailField(db_index=True, verbose_name="email address", unique=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = UserManager()

	def __str__(self):
		return self.email

	@property
	def token(self):
		return self._generate_jwt_token()

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return self.username

	def _generate_jwt_token(self):
		dt = datetime.now() + timedelta(days=60)

		token = jwt.encode({
			'id': self.pk,
			'exp':int(dt.strftime('%s'))
			}, settings.SECRET_KEY, algorithm='HS256')

		return token

	def __str__(self):
		return self.username


class Weather(models.Model):
	location = models.CharField(max_length=200)

	def __str__(self):
		return self.location