from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
@login_required
def checkout(request):
	publishKey = settings.STRIPE_PUBLISHABLE_KEY
	if request.method == 'POST':
		token = request.POST['stripeToken']
		# Create the charge on Stripe's servers -
		# this will charge the user's card
		try:
			charge = stripe.Charge.create(
				amount = 1000, # Amount in cents
				currency = "usd",
				source = token,
				description = "Example charge"
			)
		except stripe.CardError, e:
			# The card was declined
			pass

	context = { 'publishKey': publishKey }
	template = 'checkout.html'
	return render(request, template, context)