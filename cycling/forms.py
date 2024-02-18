from django import forms
from django.forms import ModelForm, TextInput, fields, widgets
from .models import Post, Profile, Comment, City
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Enter Your Post",
                "class": "form-control",
                "rows": 3,
            }
        ),
        label="",
    )
    post_image_url = forms.URLField(label="Post Image URL", required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter image URL'}))


    class Meta:
        model = Post
        fields = ("body", "post_image_url")

class CommentForm(forms.ModelForm):
    text = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Enter Your Comment",
                "class": "form-control",
                "rows": 2,
            }
        ),
        label="",
    )

    class Meta:
        model = Comment
        fields = ("text",)


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets ={
            'name' : forms.TextInput(attrs={'class' : 'input','placeholder' : 'City Name'}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User 
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_username(self):
        # Override clean_username to exclude the unique check during updates
        return self.cleaned_data['username']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs) 

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted"><small><li>Your password can\'t be similar to your other personal information</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password</li><li>Your password can’t be entirely numeric</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class ProfilePicForm(forms.ModelForm):
    profile_image_url = forms.URLField(label="Profile Image URL")
    profile_bio = forms.CharField(label="Profile Bio", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Profile Bio' }))
    homepage_link = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website Link'}))
    facebook_link = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Facebook Link'}))
    instagram_link = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instagram Link'}))
    linkedin_link = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Linkedin Link'}))

    class Meta: 
        model = Profile
        fields = ('profile_image_url',  'homepage_link', 'profile_bio', 'facebook_link', 'instagram_link', 'linkedin_link')