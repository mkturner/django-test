from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from .forms import contactForm

# Create your views here.
def contact(request):
	title = 'Contact Form'
	form = contactForm(request.POST or None)
	context = {'title': title, 'form': form }

	if form.is_valid():
		name = form.cleaned_data['name']
		comment = form.cleaned_data['comment']
		confirm_msg = None
		
		# TELL WHO IS EMAILING
		subject = '%s is trying to reach you' %(name)
		
		# NOW WHERE TO SEND REPLIES
		email_from = form.cleaned_data['email']

		# WHERE TO DELIVER THEIR MESSAGE
		email_to = [settings.EMAIL_HOST_USER]

		# OK WHAT ARE THEY SAYING
		message ='%s (%s) says: \n\n%s' %(name, email_from, comment)
		
		# NOW DELIVER IT, MINIONS
		send_mail(subject, message, email_from,	email_to, fail_silently=False)

		# CONFIRM MESSAGE SENT, SWITCH CONTEXT
		form = None
		confirm_title = 'Thanks'
		confirm_msg = 'Thanks for reaching out.'
		context = {'title':confirm_title, 'form':form, 'confirm_msg':confirm_msg}

	template = 'contact.html'
	return render(request, template, context)