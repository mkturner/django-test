from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from .forms import contactForm

# Create your views here.
def contact(request):
	form = contactForm(request.POST or None)
	if form.is_valid():
		name = form.cleaned_data['name']
		comment = form.cleaned_data['comment']
		subject = "%s is trying to reach you" %(name)
		message ='%s says: \n\n%s' %(name, comment)
		email_from = form.cleaned_data['email']
		email_to = [settings.EMAIL_HOST_USER]
		send_mail(subject, message, email_from,	email_to, fail_silently=False)
	context = locals()
	template = 'contact.html'
	return render(request, template, context)