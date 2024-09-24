from django.shortcuts import render, redirect
from .forms import BloodRequestForm
from .models import BloodRequest
from user.models import User

def home(request):
    donors = User.objects.filter(last_donation_date__isnull=False)
    return render(request, 'request/home.html', {'donors': donors})

def request_blood(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requester = request.user
            blood_request.save()
            return redirect('dashboard')
    else:
        form = BloodRequestForm()
    return render(request, 'request/request_blood.html', {'form': form})

# request/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BloodRequest
from user.models import DonationHistory
from django.utils import timezone

@login_required
def dashboard(request):
    # Display all requests regardless of status
    requests = BloodRequest.objects.all()

    # Fetch donation history specific to the logged-in user
    donation_history = DonationHistory.objects.filter(donor=request.user)

    return render(request, 'user/dashboard.html', {
        'requests': requests,
        'donation_history': donation_history
    })


@login_required
def accept_request(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)

    # Check if blood group matches
    if request.user.blood_group == blood_request.blood_group:
        # Update the accepted_by field and change status to "Completed"
        blood_request.accepted_by = request.user
        blood_request.status = 'Completed'
        blood_request.save()

        # Create a donation record in DonationHistory
        DonationHistory.objects.create(
            donor=request.user,
            recipient=blood_request.requester,
            donation_date=timezone.now()
        )

        # Update the donor's last donation date
        request.user.last_donation_date = timezone.now()
        request.user.save()
    else:
        # Handle case where blood group does not match (Optional: Show an error message)
        context = {'error': 'Blood group does not match!'}
        return render(request, 'request/accept_error.html', context)

    return redirect('dashboard')


from django.shortcuts import render
from user.models import User

from user.models import BLOOD_GROUPS

def donor_list(request):
    blood_group = request.GET.get('blood_group')
    if blood_group:
        donors = User.objects.filter(blood_group=blood_group, is_active=True)
    else:
        donors = User.objects.filter(is_active=True)

    return render(request, 'request/donor_list.html', {
        'donors': donors,
        'selected_group': blood_group,
        'BLOOD_GROUPS': BLOOD_GROUPS
    })
