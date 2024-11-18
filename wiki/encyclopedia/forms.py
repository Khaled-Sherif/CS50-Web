from django import forms


class NewArticleForm(forms.Form):
    """User Input for the title and entry to be saved"""
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Title',
        'style': 'width: 300px;',
        'class': 'form-control'
        }))
    article = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Pargraph....',
        'style': 'width: 800px; height: 400px;',
        'class': 'form-control'
        }))


class TitelDisabled(NewArticleForm):
    """Disable user to update entrys titel"""
    title_disabled = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Title',
        'style': 'width: 300px;',
        'class': 'form-control',
        'disabled': 'disabled'
        }))
