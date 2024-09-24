from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from .models import DonationHistory
from request.models import BloodRequest
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.urls import reverse,reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.edit import FormView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .forms import UserRegistrationForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views import View

class UserRegistrationView(FormView):
    template_name = 'user/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Set user as inactive for email verification
        user.save()

        # Generate activation token
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Prepare activation email
        current_site = get_current_site(self.request)
        activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        activation_url = f"http://{current_site.domain}{activation_link}"

        subject = 'Activate your account'
        html_message = render_to_string('user/activation_email.html', {
            'user': user,
            'activation_url': activation_url
        })

        # Send HTML email using EmailMultiAlternatives
        email = EmailMultiAlternatives(
            subject,
            '',  # Plain text message (optional, can be empty)
            'from@example.com',  # Sender email address (update with your email)
            [user.email]  # Recipient email address
        )
        email.attach_alternative(html_message, "text/html")  # Attach HTML content
        email.send()

        return super().form_valid(form)


User = get_user_model()

class ActivateAccountView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            # Decode the user's ID from the base64 string
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        token_generator = PasswordResetTokenGenerator()

        if user is not None and token_generator.check_token(user, token):
            # Activate the user if the token is valid
            user.is_active = True
            user.save()

            messages.success(request, 'Your account has been activated successfully! You can now log in.')
            return redirect(reverse_lazy('login'))
        else:
            # If the token is invalid, show an error message
            messages.error(request, 'The activation link is invalid or has expired.')
            return render(request, 'user/activation_invalid.html')


class UserLoginView(LoginView):
    template_name='user/login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages



def logout_view(request):
    logout(request)
    return redirect('home')



from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import UserProfileForm, CustomPasswordChangeForm

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user)
        password_form = CustomPasswordChangeForm(user, request.POST)
        
        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)  # Keep the user logged in after password change
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        profile_form = UserProfileForm(instance=user)
        password_form = CustomPasswordChangeForm(user)
    
    return render(request, 'user/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })
