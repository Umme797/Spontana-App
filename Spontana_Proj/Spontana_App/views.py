from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from Spontana_App.models import Activity, MoodTimeEntry, UserProfile, ActivityJournal, EmailVerification
import random
from datetime import timedelta
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import FullRegisterForm
from django.core.mail import send_mail
from django.contrib import messages



# Create your views here.



# HOME PAGE RELATED VIEWS

def convert_duration_string(duration_str):
    mapping = {
        "15 minutes": timedelta(minutes=15),
        "20 minutes": timedelta(minutes=20),
        "30 minutes": timedelta(minutes=30),
        "45 minutes": timedelta(minutes=45),
        "1 hour": timedelta(hours=1),
        "1.5 hours": timedelta(hours=1, minutes=30),
    }
    return mapping.get(duration_str)



def home(request):
    moods = [
        ("Energetic", "⚡"), ("Adventurous", "🧗"), ("Playful", "🎮"),
        ("Chill", "🌿"), ("Peaceful", "🧘"), ("Artistic", "🎨"),
        ("Imaginative", "🧠"), ("Curious", "🔍"), ("Inspired", "💡"),
        ("Ambitious", "🚀"), ("Studious", "📚"), ("Organized", "🗂️"),
        ("Friendly", "😊"), ("Outgoing", "🥳"), ("Restless", "😵"),
        ("Uninspired", "😶"), ("Stuck", "🪨"), ("Wandering", "🌍"),
        ("Overwhelmed", "😩"), ("Anxious", "😟"), ("Tired", "😴"),
        ("Needing a Break", "☕"),
    ]

    durations = [
        "15 minutes", "20 minutes", "30 minutes", "45 minutes",
        "1 hour", "1.5 hours",
    ]

    if request.method == "POST":
        selected_mood = request.POST.get('selected_mood')
        selected_duration_str = request.POST.get('selected_duration')
        selected_duration = convert_duration_string(selected_duration_str)

        if not selected_duration:
            return render(request, 'home.html', {
                'moods': moods,
                'durations': durations,
                'error': "Invalid time selected."
            })

        try:
            mood_time_entry = MoodTimeEntry.objects.get(mood=selected_mood, duration=selected_duration)
            matching_activities = Activity.objects.filter(mood_entry=mood_time_entry)

            if matching_activities.exists():
                random_activity = random.choice(list(matching_activities))
                return redirect('activity_detail', aid=random_activity.id)
            else:
                return render(request, 'home.html', {
                    'moods': moods,
                    'durations': durations,
                    'error': "No activity found for the selected mood and time."
                })

        except MoodTimeEntry.DoesNotExist:
            return render(request, 'home.html', {
                'moods': moods,
                'durations': durations,
                'error': "No entry matches your mood and time."
            })

    return render(request, 'home.html', {
        'moods': moods,
        'durations': durations,
    })



def activity_detail(request, aid):
    activity = get_object_or_404(Activity, id=aid)
    return render(request, 'activity_detail.html', {'activity': activity})






# USER PROFILE RELATED VIEWS
@login_required
def user_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    adventure_count = ActivityJournal.objects.filter(user=request.user).count()

    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        image = request.FILES.get('profile_image')

        profile.bio = bio
        if image:
            profile.image = image
        profile.save()

        return redirect('/user_profile')

    return render(request, 'user_profile.html', {
        'user': request.user,
        'profile': profile,
        'adventure_count': adventure_count,
    })






# ACTIVITY JOURNAL RELATED VIEWS

@login_required
def activity_journal(request):
    journals = ActivityJournal.objects.filter(user=request.user).order_by('-date')
    return render(request, 'activity_journal.html', {'journals': journals})



@login_required
def add_journal(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        title = request.POST.get('title')
        date = request.POST.get('date')
        description = request.POST.get('description')
        mood = request.POST.get('mood')
        duration = request.POST.get('duration')
        
        existing_entry = ActivityJournal.objects.filter(
            user=request.user,
            title__iexact=title.strip(),
            date=date
        ).first()

        if existing_entry:
            return render(request, 'add_journal.html', {
                'error': 'You have already added an activity with the same title on this date.'
            })

        journal = ActivityJournal.objects.create(
            user=request.user,
            image=image,
            title=title,
            date=date,
            description=description,
            mood=mood,
            duration=duration,
        )
        return redirect('/activity_journal/')

    return render(request, 'add_journal.html')






# USER AUTHENTICATION RELATED VIEWS

def login_view(request):
    if request.user.is_authenticated:
        return redirect("/home")

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "Please fill all the fields.")
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/home")
        else:
            messages.error(request, "Invalid Username or Password.")
            return render(request, 'login.html')

    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('/login')



def verify_email(request, email):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        try:
            verification = EmailVerification.objects.get(email=email)
            if verification.code == entered_code:
                return HttpResponse("✅ Email verified. You may now continue registration.")
            else:
                return HttpResponse("❌ Invalid verification code.")
        except EmailVerification.DoesNotExist:
            return HttpResponse("⚠️ Verification not found.")
    return render(request, 'verify.html', {'email': email})



def full_register(request):
    if request.method == 'POST':
        form = FullRegisterForm(request.POST)
        email = request.POST.get('email')
        action = request.POST.get('action')

        if action == "send_code":
            # Validate email format and send code
            if form.is_valid():
                code = str(random.randint(100000, 999999))
                EmailVerification.objects.update_or_create(email=email, defaults={'code': code})
                send_mail(
                    'Your Spontana Verification Code',
                    f'Your verification code is: {code}',
                    'noreply@spontana.com',
                    [email],
                    fail_silently=False,
                )
                messages.success(request, f'📧 Verification code sent to {email}')
            else:
                messages.error(request, "Invalid email format.")

        elif action == "register":
            if form.is_valid():
                username = form.cleaned_data['username']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                code_entered = form.cleaned_data['code']

                # Validate passwords
                if password1 != password2:
                    messages.error(request, "❌ Passwords do not match.")
                elif User.objects.filter(username=username).exists():
                    messages.error(request, "❌ Username already exists.")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, "❌ Email already registered.")
                else:
                    try:
                        verification = EmailVerification.objects.get(email=email)
                        if verification.code == code_entered:
                            # All good, create user
                            user = User.objects.create_user(username=username, email=email, password=password1)
                            user.save()
                            verification.delete()
                            messages.success(request, "✅ Registered successfully! You can now log in.")
                            return redirect('/login')
                        else:
                            messages.error(request, "❌ Invalid verification code.")
                    except EmailVerification.DoesNotExist:
                        messages.error(request, "⚠️ No verification code sent to this email.")
            else:
                messages.error(request, "Please correct the form errors.")
    else:
        form = FullRegisterForm()

    return render(request, 'register.html', {'form': form})

