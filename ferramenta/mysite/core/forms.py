from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'pdf', 'cover')


class Leitor(forms.Form):
    text_area = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols':55, 'rows':10}), label='')

