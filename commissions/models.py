from django.db import models
from datetime import datetime
from django.urls import reverse
from user_management.models import Profile

class Commission(models.Model):
    OPEN = 1
    FULL = 2
    COMPLETED = 3
    DISCONTINUED = 4
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    STATUS_CHOICES = (
        (OPEN, "Open"),
        (FULL, "Full"),
        (COMPLETED, "Completed"),
        (DISCONTINUED, "Discontinued")
    )
    status = models.IntegerField(
        choices = STATUS_CHOICES,
        default = OPEN
    )
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT
    )
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('commissions:commission_detail', args=[str(self.pk)])


    class Meta:
        ordering = ['created_on']

class Job(models.Model):
    OPEN = 1
    FULL = 2
    STATUS_CHOICES = (
        (OPEN, "Open"),
        (FULL, "Full"),
    )
    
    commission = models.ForeignKey(
        Commission,
        related_name="jobs",
        on_delete=models.CASCADE
    )
    
    role = models.CharField(max_length=255)
    manpower_required = models.IntegerField()
    current_manpower = models.IntegerField(default=0)
    open_manpower = models.IntegerField(default=0)
    status = models.IntegerField(
        choices = STATUS_CHOICES,
        default = OPEN,
    )


    def __str__(self):
        return self.role
    
    def modify_open_manpower(self, value):
        self.open_manpower = value
        self.save()
    
    def modify_current_manpower(self, value):
        self.current_manpower = value
        self.modify_open_manpower(self.manpower_required-value)
        self.save()
    
    
    class Meta:
        ordering = ['-status', '-manpower_required', 'role']

class JobApplication(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="job_application"
    )
    
    applicant = models.ForeignKey(
        Profile,
        related_name="job_application",
        on_delete=models.CASCADE
    )
    
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2
    
    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected")
    )
    
    status = models.IntegerField(
        choices = STATUS_CHOICES,
        default = PENDING,
    )
    
    applied_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-status', '-applied_on']

    