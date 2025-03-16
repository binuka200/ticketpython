from django.db import models
from django.contrib.auth.models import User


class TicketType(models.Model):
    type = models.CharField(max_length=200)
    desciption = models.TextField()

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Ticket Type"
        verbose_name_plural = "Ticket Types"


class Department(models.Model):
    department = models.CharField(max_length=200)
    desciption = models.TextField()

    def __str__(self):
        return self.department


class Status(models.Model):
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.status


class Ticket(models.Model):
    class TicketPriority(models.IntegerChoices):
        HIGH = 1, "High"
        MEDIUM = 2, "Medium"
        LOW = 3, "Low"

    PRIORITY_CHOICES = [
        ("HIGH", "High"),
        ("MEDIUM", "Medium"),
        ("LOW", "Low"),
    ]
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_tickets")
    type = models.ForeignKey(
        TicketType, on_delete=models.SET_NULL, null=True, blank=True
    )
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.ForeignKey(
        Status, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.IntegerField(
        choices=TicketPriority.choices, default=TicketPriority.HIGH
    )
    assigned = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_tickets",
    )
    followers = models.ManyToManyField(
        User, blank=True, related_name="followed_tickets"
    )
    sentiment = models.CharField(max_length=200, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-updated"]


class TicketPost(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="posts")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="ticket_posts",
        null=True,
        blank=True,
    )
    message = models.TextField(max_length=200)
    tmp_message = models.TextField(blank=True, null=True)
    private = models.BooleanField(default=False)
    upload = models.FileField(
        upload_to="ticket_uploads/", blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ["-created"]
