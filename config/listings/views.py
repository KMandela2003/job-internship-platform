from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm, OpportunityForm
from .models import Application, Opportunity

def home_view(request):
    opportunities = Opportunity.objects.all()
    query = request.GET.get('q', '').strip()
    opp_type = request.GET.get('type', '').strip()

    if query:
        opportunities = opportunities.filter(
            Q(title__icontains=query) | Q(company__icontains=query) | Q(location__icontains=query)
        )
    if opp_type in ('JOB', 'INTERNSHIP'):
        opportunities = opportunities.filter(opportunity_type=opp_type)

    return render(request, 'listings/home.html', {
        'opportunities': opportunities,
        'query': query,
        'selected_type': opp_type,
    })


def opportunity_detail_view(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    already_applied = False
    if request.user.is_authenticated:
        already_applied = Application.objects.filter(opportunity=opportunity, applicant=request.user).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        if already_applied:
            messages.warning(request, 'You have already applied for this opportunity.')
            return redirect('opportunity_detail', pk=pk)

        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.opportunity = opportunity
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully.')
            return redirect('opportunity_detail', pk=pk)
    else:
        form = ApplicationForm()

    return render(request, 'listings/opportunity_detail.html', {
        'opportunity': opportunity,
        'form': form,
        'already_applied': already_applied,
    })


@login_required
def create_opportunity_view(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.posted_by = request.user
            opportunity.save()
            messages.success(request, 'Opportunity posted successfully.')
            return redirect('home')
    else:
        form = OpportunityForm()

    return render(request, 'listings/opportunity_form.html', {'form': form})


@login_required
def dashboard_view(request):
    posted_opportunities = Opportunity.objects.filter(posted_by=request.user)
    my_applications = Application.objects.filter(applicant=request.user).select_related('opportunity')
    return render(request, 'listings/dashboard.html', {
        'posted_opportunities': posted_opportunities,
        'my_applications': my_applications,
    })


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})