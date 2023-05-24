from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TicketManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        if len(postData["event_id"]) < 1:
            errors["event_id"] = "Please select an event"
            
        if len(postData["section"]) < 1:
            errors["section"] = "Please select a section"
            
        if len(postData["number"]) < 1:
            errors["number"] = "Please select a number of tickets"
        return errors

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateField()
    event_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, through='Tickets')
    
class Tickets(models.Model):
    event = models.ForeignKey(Event, related_name="tickets", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="tickets", on_delete=models.CASCADE)
    section = models.CharField(max_length=200)
    number = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TicketManager()
    

class ContactManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors["name"] = "Name should be at least 1 characters"
        if len(postData['email']) < 1:
            errors["email"] = "Email should be at least 1 characters"
        if len(postData['message']) < 1:
            errors["message"] = "Message should be at least 1 characters"
        return errors

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ContactManager()
