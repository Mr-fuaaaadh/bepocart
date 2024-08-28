from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_order_email(order):
    subject = f"New Order Received: {order.id}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['contact@bepocart.com']

    # Render the HTML template with the order context
    html_content = render_to_string('order_email.html', {'order': order})

    # Create an EmailMultiAlternatives object
    email = EmailMultiAlternatives(
        subject=subject,
        body='This is an HTML email. Please use an email client that supports HTML.',
        from_email=from_email,
        to=recipient_list,
    )
    
    # Attach the HTML content
    email.attach_alternative(html_content, "text/html")

    # Send the email 
    email.send()
