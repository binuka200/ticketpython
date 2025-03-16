from django.core.mail import send_mass_mail
from django.conf import settings
from django.contrib.auth.models import User
from typing import Set
from django.urls import reverse


def send_ticket_update_notification(ticket, new_post, exclude_user=None):

    users_to_notify: Set[User] = set()

    if ticket.created_by and ticket.created_by != exclude_user:
        users_to_notify.add(ticket.created_by)

    if ticket.assigned and ticket.assigned != exclude_user:
        users_to_notify.add(ticket.assigned)

    for follower in ticket.followers.all():
        if follower != exclude_user:
            users_to_notify.add(follower)

    ticket_url = reverse('view_ticket', kwargs={'pk': ticket.id})

    subject = f'Ticket #{ticket.id} Update: {ticket.title}'
    message = f'''A new response has been added to ticket #{ticket.id}
    
Title: {ticket.title}
Updated by: {new_post.user.username if new_post.user else 'Unknown'}
Message:
{new_post.message}

View ticket: {ticket_url}
'''

    email_data = [
        (
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        for user in users_to_notify
        if user.email  # Only send to users with email addresses
    ]

    # Send emails
    if email_data:
        try:
            send_mass_mail(email_data, fail_silently=False)
        except Exception as e:
            # Log the error but don't raise it to prevent disrupting the user experience
            print(f"Error sending email notifications: {str(e)}")
