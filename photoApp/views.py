from django.shortcuts import render, get_object_or_404
from .models import CustomUser, Photo,Profile, Tag
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserUpdateForm, ProfileUpdateForm, ChangePasswordForm
from cloudinary.uploader import upload
import random

# Create your views here.

def home(request):
    photos = Photo.objects.all().prefetch_related('tags', 'likes')  # Fetch related tags and likes efficiently
    tags = Tag.objects.all()
    
    return render(request, 'gallery.html', {"photos": photos, "tags": tags})

    
def filter_photos(request, tag_name):
    selected_tag = get_object_or_404(Tag, name=tag_name)
    photos = Photo.objects.filter(tags=selected_tag).prefetch_related('tags', 'likes')  
    tags = Tag.objects.all()

    return render(request, "gallery.html", {"photos": photos, "selected_tag": selected_tag, "tags": tags})


def view_photo(request, pk):
    photo = photo = get_object_or_404(Photo,id=pk)
    colors = ["green-500", "blue-500", "yellow-400", "red-500", "purple-500", "orange-500"]
    
    tag_list = [{"name": tag.name, "color": random.choice(colors)} for tag in photo.tags.all()]
    
    return render(request, 'view_photo.html', {'photo':photo, 'tags':tag_list})

User = get_user_model()

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return render(request, "register.html")

        if password == password2:
            user = User.objects.create_user(email=email, password=password,username=username)
            return redirect("login")
        else:
            messages.error(request, "Passwords doesn't match")
            return render(request, "register.html")
    return render(request, "register.html")


def custom_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials!")
            return render(request, "login.html")
    return render(request, "login.html")


def custom_logout(request):
    logout(request)
    return redirect("login")

@login_required
def profile(request):
    user = request.user
    
    # Ensure profile exists
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)  # Use `profile` instead of `request.user.profile`

        if u_form.is_valid() and p_form.is_valid():
            # Upload image to Cloudinary with transformation
            image = request.FILES.get('image')
            if image:
                uploaded_image = upload(image, width=300, height=300, crop="fill", quality="80")
                profile.image = uploaded_image['secure_url']  # Use `profile` instead of `request.user.profile`

            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'profile.html', context)

@login_required
def update_password(request):
    current_user = request.user

    if request.method == 'POST':
        form = ChangePasswordForm(current_user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been updated, Please Login')
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return render(request, 'profile.html', {'form': form})
    else:
        form = ChangePasswordForm(current_user)
        return render(request, 'profile.html', {'form':form})

def error_404(request, exception):
    return render(request, '404.html')

@login_required
def like_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    user = request.user

    if user in photo.likes.all():
        photo.likes.remove(user)  # Unlike
    else:
        photo.likes.add(user)  # Like

    return redirect("home") 