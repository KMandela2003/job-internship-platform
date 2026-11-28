from django.contrib.auth.models import User
from django.db import models


class Opportunity(models.Model):
    OPPORTUNITY_TYPES = [
        ('JOB', 'Job'),
        ('INTERNSHIP', 'Internship'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=150)
    opportunity_type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPES, default='INTERNSHIP')
    location = models.CharField(max_length=150)
    description = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opportunities', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.company} ({self.get_opportunity_type_display()})"


class Application(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_note = models.TextField()
    portfolio_url = models.URLField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('opportunity', 'applicant')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.username} -> {self.opportunity.title}"