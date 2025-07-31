from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import SimpleUserCreationForm, VideoForm
from .models import Video, Comment, Like
from django.db.models import Q

def home(request):
    videos = Video.objects.all()
    return render(request, 'core/home.html', {'videos': videos})

def register_view(request):
    if request.method == 'POST':
        form = SimpleUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès.")
            return redirect('login') 
    else:
        form = SimpleUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Identifiants invalides")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def watch_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    comments = video.comments.all().order_by('-created_at')
    like_count = video.video_likes.count()
    is_liked = request.user.is_authenticated and video.video_likes.filter(user=request.user).exists()

    return render(request, 'core/watch.html', {
        'video': video,
        'comments': comments,
        'like_count': like_count,
        'is_liked': is_liked
    })


@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            messages.success(request, "Vidéo ajoutée avec succès.")
            return redirect('home')
    else:
        form = VideoForm()
    return render(request, 'core/upload.html', {'form': form})



@login_required
def edit_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if video.uploaded_by != request.user:
        return HttpResponse("Non autorisé", status=403)

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, "Vidéo modifiée.")
            return redirect('home')
    else:
        form = VideoForm(instance=video)
    return render(request, 'core/edit.html', {'form': form, 'video': video})


@login_required
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if video.uploaded_by != request.user:
        return HttpResponse("Non autorisé", status=403)

    if request.method == 'POST':
        video.delete()
        messages.success(request, "Vidéo supprimée.")
        return redirect('home')
    return render(request, 'core/delete.html', {'video': video})


@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    like, created = Like.objects.get_or_create(user=request.user, video=video)

    if not created:
        # L'utilisateur a déjà liké => on supprime le like
        like.delete()
    # sinon, le like a été créé automatiquement avec get_or_create

    return redirect('watch_video', video_id=video.id)


@login_required
def add_comment(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.method == 'POST':
        text = request.POST.get('content')
        if text:
            Comment.objects.create(video=video, user=request.user, text=text)
    return redirect('watch_video', video_id=video.id)


def video_search(request):
    query = request.GET.get('q')
    videos = Video.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ) if query else []

    return render(request, 'core/search_results.html', {
        'videos': videos,
        'query': query
    })
