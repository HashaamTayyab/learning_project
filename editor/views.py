from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from .models import Track, Dot, SubDot, Topic
from django import forms
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from .forms import TrackForm, DotForm, SubDotForm, TopicForm, ContentForm

# Create your views here.

# Editor Dashboard

def editor_dashboard(request):
    tracks = Track.objects.all()
    return render(request, 'editor/dashboard.html', {'tracks': tracks})

# View Dots

def view_Dots(request, track_id):
    track = Track.objects.get(id=track_id)
    Dots = Dot.objects.filter(track=track)
    return render(request, 'editor/Dots.html', {'track': track, 'Dots': Dots})

# View Subdots

def view_subdots(request, Dot_id):
    dot_instance = Dot.objects.get(id=Dot_id)
    subdots = SubDot.objects.filter(dot=dot_instance)
    return render(request, 'editor/subdots.html', {'Dot': dot_instance, 'subdots': subdots})

# View Topics

def view_topics(request, subdot_id):
    subdot = SubDot.objects.get(id=subdot_id)
    topics = Topic.objects.filter(subdot=subdot)
    return render(request, 'editor/topics.html', {'subdot': subdot, 'topics': topics})

# View Topic Details

def view_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    return render(request, 'editor/topic_detail.html', {'topic': topic})

# Subscription View

def subscribe_editor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        User = get_user_model()

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'You are already registered. Please log in.')
            return render(request, 'editor/subscribe.html', {'error_message': 'You are already registered. Please log in.'})

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Registration successful! You can now add content.')
        return redirect('content_addition')  # Redirect to the content addition page
    return render(request, 'editor/subscribe.html')

# Login View

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('content_addition')  # Redirect to the content addition page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'editor/login.html')

# New view for content addition

def content_addition(request):
    if not request.user.is_authenticated:
        messages.error(request, "You're not registered. Please sign up to add content.")
        return redirect('signup')  # Redirect to the signup page
    Dots = Dot.objects.all()  # Fetch all Dots
    subdots = SubDot.objects.all()  # Fetch all subdots
    return render(request, 'editor/content_addition.html', {'Dots': Dots, 'subdots': subdots})

# Registration View

def register(request):
    if request.method == 'POST':
        # Handle registration logic here
        pass
    return render(request, 'editor/register.html')

# Content Upload Form

class ContentForm(forms.Form):
    title = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea)
    code = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False)
    audio = forms.FileField(required=False)

# Content Upload View

def upload_content(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            code = form.cleaned_data['code']
            image = form.cleaned_data['image']
            audio = form.cleaned_data['audio']
            # Save files and content to the database
            fs = FileSystemStorage()
            if image:
                try:
                    fs.save(image.name, image)
                except ValidationError:
                    form.add_error('image', 'Invalid image file.')
            if audio:
                try:
                    fs.save(audio.name, audio)
                except ValidationError:
                    form.add_error('audio', 'Invalid audio file.')
            # Save content to the database
            new_topic = Topic(title=title, content=content, code=code)
            new_topic.save()
            return redirect('editor_dashboard')
    else:
        form = ContentForm()
    return render(request, 'editor/upload_content.html', {'form': form})

# Add Topic View

def add_topic(request, subdot_id):
    subdot = SubDot.objects.get(id=subdot_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        explanation_type = request.POST.get('explanation_type')
        content = request.POST.get('content')
        code = request.POST.get('code')
        
        # Handle file uploads
        image = request.FILES.get('image')
        audio = request.FILES.get('audio')
        
        # Create a new topic
        topic = Topic(
            subdot=subdot,
            title=title,
            content=content,
            code=code
        )
        
        # Save the topic first to get an ID
        topic.save()
        
        # Handle image upload
        if image:
            # Generate a unique filename
            ext = image.name.split('.')[-1]
            filename = f'topic_{topic.id}_image.{ext}'
            topic.image.save(filename, image, save=True)
            
        # Handle audio upload
        if audio:
            # Generate a unique filename
            ext = audio.name.split('.')[-1]
            filename = f'topic_{topic.id}_audio.{ext}'
            topic.audio.save(filename, audio, save=True)

        messages.success(request, 'Topic added successfully!')
        return redirect('view_topics', subdot_id=subdot.id)
    return render(request, 'editor/add_topic.html', {'subdot': subdot})

# Add Subdot View

def add_subdot(request, Dot_id):
    dot_instance = Dot.objects.get(id=Dot_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        subdot = SubDot(dot=dot_instance, name=name)
        subdot.save()
        messages.success(request, 'Subdot added successfully!')
        return redirect('view_subdots', Dot_id=dot_instance.id)
    return render(request, 'editor/add_subdot.html', {'Dot': dot_instance})
