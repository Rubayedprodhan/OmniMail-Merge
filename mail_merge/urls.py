from django.urls import path
from .views import email_merge_view

urlpatterns = [
    path('', email_merge_view, name='mail_merge'),
]