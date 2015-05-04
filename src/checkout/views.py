from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
@login_required
def checkout(request):
	publishKey = settings.STRIPE_PUBLISHABLE_KEY
	customer_id = request.user.userstripe.stripe_id
	if request.method == 'POST':
		token = request.POST['stripeToken']
		# Create the charge on Stripe's servers -
		# this will charge the user's card
		try:
			# associate patment source (token) with customer 
			# for future purchases
			customer = stripe.Customer.retrieve(customer_id)
			customer.sources.create(source=token)
			# charge the card
			charge = stripe.Charge.create(
				amount = 1000, # Amount in cents
				currency = "usd",
				customer = customer,
				description = "Example charge"
			)
		except stripe.CardError, e:
			# The card was declined
			pass

	context = { 'publishKey': publishKey }
	template = 'checkout.html'
	return render(request, template, context)