from django.db import models
from django.conf import settings

from allauth.account.signals import user_logged_in, user_signed_up

# Create your models here.

class profile(models.Model):
	name = models.CharField(max_length = 1200)
	description = models.TextField(default = 'description default')
	user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)

	def __unicode__(self):
		return self.name

class userStripe(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	stripe_id = models.CharField(max_length=200, null=True, blank=True)

	def __unicode__(self):
		if self.stripe_id:
			return str(self.stripe_id)
		else:
			return self.user.username

def stripe_callback(sender, request, user, **kwargs):
    idStripe, created = userStripe.objects.get_or_create(user = user)
    if created:
    	print 'created for %s'%(user.username)

def profile_callback(sender, request, user, **kwargs):
    userProfile, isCreated = profile.objects.get_or_create(user = user)
    if isCreated:
    	userProfile.name = user.username
    	userProfile.save()

user_logged_in.connect(stripe_callback)
user_signed_up.connect(profile_callback)