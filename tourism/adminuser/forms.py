from django import forms
from app.models import TourPackage, Guide


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Current Password', 'required': 'required'}))
    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'New Password', 'required': 'required'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password', 'required': 'required'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError(
                "New Password and Confirm Password do not match.")

        return cleaned_data


class PackageCreationForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = ['name', 'location', 'duration', 'price',
                  'max_persons', 'description', 'image']
        labels = {
            'name': 'Package Name',
            'location': 'Location',
            'duration': 'Duration',
            'price': 'Price (USD)',
            'max_persons': 'Maximum Persons',
            'description': 'Description',
            'image': 'Image',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            # You can customize widgets as needed
        }


class GuideCreationForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ['full_name', 'designation', 'image',
                  'facebook_link', 'twitter_link', 'instagram_link']
        labels = {
            'full_name': 'Full Name',
            'designation': 'Designation',
            'image': 'Image',
            'facebook_link': 'Facebook Link',
            'twitter_link': 'Twitter Link',
            'instagram_link': 'Instagram Link',
        }


