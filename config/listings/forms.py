from django import forms
from .models import Application, Opportunity


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['title', 'company', 'opportunity_type', 'location', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_note', 'portfolio_url']
        widgets = {
            'cover_note': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Briefly explain why you are a good fit...'}),
            'portfolio_url': forms.URLInput(attrs={'placeholder': 'https://github.com/yourusername'}),
        }