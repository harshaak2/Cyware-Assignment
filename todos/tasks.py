from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_task_creation_email(task_title, user_email):
  subject = 'New Task Created'
  message = f'A new task "{task_title}" has been created in your todo list.'
  send_mail(
    subject, 
    message,
    settings.DEFAULT_EMAIL_FROM,
    [user_email],
    fail_silently=False,
  )

@shared_task
def send_list_creation_email(list_title, user_email):
  subject = 'New List Created'
  message = f'A new todo list "{list_title}" has been created.'
  send_mail(
    subject,
    message,
    settings.DEFAULT_EMAIL_FROM,
    [user_email],
    fail_silently=False,
  )