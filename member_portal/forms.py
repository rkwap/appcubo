from django import forms
import datetime

class addfeed_form(forms.Form):
    title = forms.CharField(
        label='Title',
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Enter title', 'class' : 'form-control'}),
        required = True
        )
    CATEGORY_CHOICES = (
        ("NR", "New Release"),
        ("DI", "Discovery"),
        ("UP", "Update"),
        ("BF", "Bugs and Fixes"),
        ("PD", "Price Drop"),
    )
    category = forms.CharField(
        label='Type of Feed',
        widget=forms.Select(attrs={'class':'form-control'},choices=CATEGORY_CHOICES),
        required=True
        )

    content = forms.CharField(
        label='Content',
        widget=forms.Textarea(attrs={'placeholder': 'Content', 'class' : 'form-control'}),
        required=True
        )

    screenshots = forms.ImageField(
        label='Screen Shots',
        required = False
        )

    tags = forms.CharField(
        label='tags', 
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Enter title', 'class' : 'form-control'}),
        required = True
        )
