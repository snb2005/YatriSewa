import requests
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from .forms import UserRegistrationForm, ProfileUpdateForm, CustomPasswordChangeForm
from .models import Profile
from .models import Accommodation,Booking 
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from .models import Booking
from .models import EmergencyContact
from .models import SOSRequest
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import EmergencyAnnouncement
from django.http import HttpResponse
from django.http import JsonResponse
from .models import LostAndFound
from .forms import LostAndFoundForm
# from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save user
            phone_number = form.cleaned_data.get('phone_number')
            address = form.cleaned_data.get('address')

            # Use get_or_create to ensure profile is created
            profile, created = Profile.objects.get_or_create(user=user)

            # Update profile fields
            profile.phone_number = phone_number
            profile.address = address
            profile.save()

            messages.success(request, "Registration successful!")
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
def index(request):
    return render(request,'index.html')

def accomodations(request):
    return render(request, 'accomodations.html')

def experiences(request):
    return render(request, 'experiences.html')

def tours(request):
    return render(request, 'tours.html')

def shahisnan(request):
    return render(request, 'shahisnan.html')

def sample(request):
    return render(request, 'sample.html')

def logout_view(request):
    logout(request)
    return redirect('login')
def hotel1(request):
    return render(request,'hotel1.html')
def hotel2(request):
    return render(request,'hotel2.html')
def hotel3(request):
    return render(request,'hotel3.html')
def hotel4(request):
    return render(request,'hotel4.html')
def hotel5(request):
    return render(request,'hotel5.html')
def hotel6(request):
    return render(request,'hotel6.html')

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)  # Get the user's profile
    bookings = Booking.objects.filter(user=request.user)  # Get user's bookings

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
        
    return render(request, 'profile.html', {'form': form, 'bookings': bookings})  # Pass bookings to template

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully!")
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, "This email address is not registered with any account.")
            return self.form_invalid(form)
        return super().form_valid(form)
    
def send_otp(phone_number):
    api_key = settings.TWO_FACTOR_API_KEY
    url = f"https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/AUTOGEN"
    response = requests.get(url)
    data = response.json()
    return data

def verify_otp(session_id, otp_input):
    api_key = settings.TWO_FACTOR_API_KEY
    url = f"https://2factor.in/API/V1/{api_key}/SMS/VERIFY/{session_id}/{otp_input}"
    response = requests.get(url)
    data = response.json()
    return data

# Step 1: Registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')

            # Step 2: Send OTP
            otp_response = send_otp(phone_number)
            if otp_response['Status'] == 'Success':
                request.session['otp_session_id'] = otp_response['Details']  # Save session ID
                request.session['user_data'] = form.cleaned_data  # Temporarily save form data

                # Redirect to OTP verification page
                return redirect('verify_otp')
            else:
                messages.error(request, "Failed to send OTP. Try again.")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

# Step 3: OTP Verification
def verify_otp_view(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        otp_session_id = request.session.get('otp_session_id')

        # Verify OTP
        otp_verify_response = verify_otp(otp_session_id, otp_input)

        if otp_verify_response['Status'] == 'Success':
            # OTP Verified. Now create the user
            user_data = request.session.get('user_data')
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password1']
            )
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone_number = user_data['phone_number']
            profile.address = user_data['address']
            profile.save()

            messages.success(request, "Registration successful! You can now login.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'verify_otp.html')

def success_view(request):
    return render(request, 'success.html')  # Ensure this template exists

def accommodations(request):
    accommodations = Accommodation.objects.all()  # Get all accommodations
    return render(request, 'accommodations.html', {'accommodations': accommodations})

@login_required
def book_accommodation(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)

    # Create a booking entry
    Booking.objects.create(user=request.user, accommodation=accommodation)

    messages.success(request, "Your booking has been confirmed!")
    return redirect('accommodations')  # Redirect to the accommodations page or any other page you prefer


@login_required
def book_accommodation(request, accommodation_id):
    accommodation = Accommodation.objects.get(id=accommodation_id)
    if request.method == 'POST':
        checkin_date = request.POST['checkin_date']
        checkout_date = request.POST['checkout_date']
        guests = request.POST['guests']
        
        Booking.objects.create(
            user=request.user,
            accommodation=accommodation,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            guests=guests
        )
        return redirect('booking_success', accommodation_id=accommodation.id)
    
    return render(request, 'booking.html', {'accommodation': accommodation})

def number_of_days(checkin_date, checkout_date):
    checkin = datetime.strptime(checkin_date, '%Y-%m-%d')
    checkout = datetime.strptime(checkout_date, '%Y-%m-%d')
    return (checkout - checkin).days


def process_payment(request, accommodation_id):
    if request.method == 'POST':
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        guests = request.POST.get('guests')

        checkin = datetime.strptime(checkin_date, '%Y-%m-%d')
        checkout = datetime.strptime(checkout_date, '%Y-%m-%d')

        if checkout < checkin:
            messages.error(request, "Check-out date must be greater than or equal to check-in date.")
            return redirect('book_accommodation', accommodation_id=accommodation_id)

        # Proceed with booking logic (save to the database, etc.)
        accommodation = get_object_or_404(Accommodation, id=accommodation_id)
        # Example: save booking info to the database (implement as per your models)
        # Booking.objects.create(accommodation=accommodation, checkin_date=checkin, checkout_date=checkout, guests=guests)

        # Redirect to the booking success page
        return render(request, 'booking_success.html', {'accommodation': accommodation})

    return redirect('accommodations')  # Fallback if not a POST request

@login_required
def booking_success(request, accommodation_id, checkin_date, checkout_date, guests):
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)
    
    # Create the booking after successful payment
    booking = Booking.objects.create(
        user=request.user,
        accommodation=accommodation,
        checkin_date=checkin_date,
        checkout_date=checkout_date,    
        guests=guests
    )
    
    # Pass booking to success template
    return render(request, 'booking_success.html', {'accommodation': accommodation, 'booking': booking})

def user_profile(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)  # Filter bookings for the logged-in user
        return render(request, 'user_profile.html', {'bookings': bookings})
    return redirect('login')

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Your booking has been canceled successfully.")
    return redirect('profile')



def contact_directory(request):
    contacts = EmergencyContact.objects.all().order_by('category')
    return render(request, 'contact_directory.html', {'contacts': contacts})



def sos_request(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        location = request.POST.get('location')

        # Create and save the SOS request to the database
        sos_request = SOSRequest(user_name=user_name, location=location)
        sos_request.save()

        # Show success message in the frontend (optional)
        messages.success(request, f"New SOS Request: {user_name} at {location}")

        return HttpResponse("SOS Request received successfully!")

    return render(request, 'sos_form.html')

def sos_confirmation(request):
    return render(request, 'sos_confirmation.html')


def emergency_announcements(request):
    announcements = EmergencyAnnouncement.objects.filter(is_active=True).order_by('-date_posted')
    return render(request, 'emergency_announcements.html', {'announcements': announcements})

def timepass(request):
    return render(request,'timepass.html')

def index1(request):
    return render(request,'index1.html')



@login_required
def create_checkout_session(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)
    checkin_date = request.POST.get('checkin_date')
    checkout_date = request.POST.get('checkout_date')
    guests = request.POST.get('guests')
    
    # Calculate the total price
    num_days = (datetime.strptime(checkout_date, '%Y-%m-%d') - datetime.strptime(checkin_date, '%Y-%m-%d')).days
    total_amount = accommodation.price * num_days * int(guests)

    # Create Stripe checkout session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': accommodation.name,
                },
                'unit_amount': int(total_amount * 100),  # Stripe expects the amount in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url = request.build_absolute_uri(reverse('booking_success',args=[accommodation_id, checkin_date, checkout_date, guests])),

        cancel_url=request.build_absolute_uri(reverse('book_accommodation', args=[accommodation.id])),
    )

    # Redirect to Stripe checkout
    return JsonResponse({
        'id': checkout_session.id
    })


def tala(request):
    return render(request,'tala.html')

def tendara(request):
    return render(request,'tendara.html')

def hanbara(request):
    return render(request,'hanbara.html')
def reviews(request):
    return render(request,'reviews.html')


# List all Lost and Found items (new name for template)
def lost_and_found_list(request):
    items = LostAndFound.objects.all()
    return render(request, 'lost_and_found_list.html', {'items': items})

# Create new Lost or Found item
def create_lost_and_found(request):
    if request.method == 'POST':
        form = LostAndFoundForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lost_and_found_list')  # After submission, redirect to the new list page
    else:
        form = LostAndFoundForm()
    return render(request, 'create_lost_and_found.html', {'form': form})