from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class AccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('User must have an email!')
		if not username:
			raise ValueError('User must have a username!')
		user = self.model(
			email = self.normalize_email(email),
			username = username
		)
		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email = self.normalize_email(email),
			username = username,password=password
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.is_protected = True
		user.is_active = True
		user.save(using = self._db)
		return user

def get_profile_image_path(instance, filename):
		return str(f'profile_images/{instance.pk}/{filename}')
	
def get_cover_image_path(instance, filename):
	return str(f'cover_images/{instance.pk}/{filename}')

class Account(AbstractBaseUser):
	email = models.EmailField(max_length=254, unique=True)
	username = models.CharField(max_length=50, unique=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_protected = models.BooleanField(default=False)
	hide_email = models.BooleanField(default=False)
	profile_image = models.ImageField(upload_to=get_profile_image_path, null=True, blank=True)
	cover_image = models.ImageField(upload_to=get_cover_image_path, null=True, blank=True)
	date_joined = models.DateField(auto_now_add=True)
	last_login = models.DateField(auto_now=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username'] 

	objects = AccountManager()

	def __str__(self):
		return self.username

	def has_perm(self, *args, **kwargs):
		return True

	def has_module_perms(self, *args, **kwargs):
		return True