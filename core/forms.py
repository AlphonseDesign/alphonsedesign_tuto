# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Video

class SimpleUserCreationForm(UserCreationForm):
    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 4:
            raise ValidationError("Le mot de passe doit contenir au moins 4 caractères.")
        return password

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail']

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Titre de la vidéo'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Décris ta vidéo...'
            }),
            'video_file': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-gray-700 bg-gray-50 border border-gray-300 rounded cursor-pointer'
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-gray-700 bg-gray-50 border border-gray-300 rounded cursor-pointer'
            }),
        }
