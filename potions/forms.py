from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Potion, EmotionIngredient


class BrewerRegistrationForm(UserCreationForm):
    """Custom registration form for new alchemists joining MoodBrew."""
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'your@email.com (optional)',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Choose your alchemist name',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Create a secret passphrase',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm your passphrase',
        })


class PotionBrewForm(forms.ModelForm):
    """
    Form for brewing (creating/editing) emotional potions.
    Uses checkbox pills for ingredient selection and a range slider for vibe.
    """
    ingredients = forms.ModelMultipleChoiceField(
        queryset=EmotionIngredient.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'emotion-checkbox',
        }),
        help_text='Pick all the feelings swirling in your cauldron right now',
    )

    class Meta:
        model = Potion
        fields = ['title', 'ingredients', 'vibe_rating', 'reflection', 'is_favorite']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. "Sunday Morning Sunbeam" or "3am Overthinking Elixir"',
            }),
            'vibe_rating': forms.NumberInput(attrs={
                'class': 'form-input',
                'type': 'range',
                'min': '1',
                'max': '10',
                'step': '1',
            }),
            'reflection': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'What stirred these feelings today? Pour your thoughts here...',
            }),
            'is_favorite': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
        }

    def clean_vibe_rating(self):
        val = self.cleaned_data.get('vibe_rating')
        if val is None or val < 1 or val > 10:
            raise forms.ValidationError('Vibe must be between 1 and 10.')
        return val
