from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_user_to_group(sender, instance=None, created=False, **kwargs):
	if created:
		Group.objects.get_or_create(name="Manager")
		Group.objects.get_or_create(name="Employee")
		if instance.groups.exists() or instance.is_superuser:
			pass
		else:
			Employee_group, created = Group.objects.get_or_create(name="Employee")
			instance.groups.add(Employee_group)

class Parking_Space(models.Model):
	park_name = models.CharField(max_length=100, blank=False, null=True)
	no_of_spaces = models.IntegerField(default=2)


	class Meta:
		verbose_name_plural = 'Parking Spaces'

	def __str__(self):
		return self.park_name

	def	ft_remove_space(self):
		return self.no_of_spaces - 1
	
	def ft_add_space(self):
		return self.no_of_spaces + 1
	
	def ft_is_available(self):
		if self.no_of_spaces > 0:
			return True
		else:
			return False
	
class Bookings(models.Model):

	phone_message = 'Phone number must be entered in the format: (+7|8) 960 xxx-xx-xx ' 
	phone_regex = RegexValidator(
		regex=r'^(\+?7|8)\d{10}$',
		message=(phone_message)
	)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	manufacturer = models.CharField(max_length=100, blank=False, null=False)
	car_model = models.CharField(max_length=100, blank=False, null=False)
	color = models.CharField(max_length=100,blank=False, null=False)
	plate_number = models.CharField(max_length=100, blank=False, null=False)
	start_period = models.DateTimeField(blank=False, null=False)
	end_period = models.DateTimeField(blank=False, null=False)
	is_booked = models.BooleanField(default=False)
	ticket = models.CharField(max_length=7, blank=False, null=False)
	phone = models.CharField(validators = [phone_regex], max_length=15,blank=False, null=False)
	parking_space = models.ForeignKey(Parking_Space, on_delete=models.CASCADE)

	def __str__(self):
		return self.plate_number

	class Meta:
		verbose_name_plural = 'Bookings'
