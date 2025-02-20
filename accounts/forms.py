from .models import Profile 
from django import forms 

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class ProfileFirstNameForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name']

class ProfileLastNameForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['last_name']

class ProfileBioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

class ProfileLocationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location']

        
