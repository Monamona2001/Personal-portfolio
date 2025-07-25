from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from .models import Contact
from django.conf import settings

def home(request):
    return render(request,'home.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            # Save to database
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            # Compose message for YOU
            full_message = f"Message from {name} <{email}>:\n\n{message}"
            try:
                # 1. Send mail to YOU
                send_mail(
                    subject,
                    full_message,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )

                # 2. Send thank you mail to USER
                thank_you_subject = "Thank You for Contacting Me!"
                thank_you_message = f"Dear {name},\n\nThank you for reaching out! I’ve received your message and will get back to you soon.\n\nRegards,\nMonali"
                send_mail(
                    thank_you_subject,
                    thank_you_message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )

                return render(request, 'home.html', {'success': 'Message sent successfully!'})

            except Exception as e:
                return render(request, 'home.html', {'error': f"Error sending email: {str(e)}"})

        else:
            return render(request, 'home.html', {'error': 'All fields are required.'})

    return render(request, 'home.html')

