from django import forms


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Your plate of food')